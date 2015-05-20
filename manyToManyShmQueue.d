ckstruct ManyToManyWriter( T, int Consumers, int Capacity ) if (isPow2(Capacity)) {
  mixin ManyToManyCommon!(T, Consumers, Capacity);

  long cacheTail;
  long cacheHead;

  this(string fn) {
	 writefln("Calling initfile");
	 initFile(fn);
	 writefln("Getting head");
	 cacheHead = getHead();
	 writefln("head %s", cacheHead);
	 cacheTail = getTail();
	 writefln( "tail %s", cacheTail);
  };

loc  bool full() {
	 if ( cacheTail - cacheHead < Capacity ) return false;
	 cacheTail = getTail();
	 cacheHead = getHead();
	 //enforce( cacheTail - cacheHead <= Capacity, "Overfull queue");
	 return (cacheTail - cacheHead >= Capacity);
  };

  bool reserved = false;
  long reservedPos = long.max;

  T* reserve() {
	 enforce(!reserved);
	 reservedPos = atomicOp!"+="(header.reserveTail.value, 1) - 1;
	 while ( reservedPos - cacheHead == Capacity ) {
		cacheHead = getHead();
	 };
	 reserved = true;
	 return &data[indexOf(reservedPos)];
  };

  void commit() {
	 enforce(reserved);
	 while ( !cas( &header.commitTail.value, reservedPos, reservedPos + 1 ) ) {};
	 cacheTail = reservedPos + 1;
	 reserved = false;
	 reservedPos = long.max;
  };
};
