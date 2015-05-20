version (X86_64)
{
  T atomicOp(string s : "+=", T)(ref shared T val, T mod) pure nothrow @nogc
	 if (__traits(isIntegral, T))
		{
        T oval = void;
        static if (T.sizeof == 8)
          {
            asm pure nothrow @nogc
              {
                mov RAX, mod;
                mov RDX, val;
                lock;
                xadd[RDX], RAX;
                mov oval, RAX;
              }
          }
        return oval + mod;
		}
}