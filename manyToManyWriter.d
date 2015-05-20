struct ManyToManyWriter( T, int Consumers, int Capacity ) if (isPow2(Capacity)) {
  mixin ManyToManyCommon!(T, Consumers, Capacity);

  long cacheTail;
  long cacheHead;

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
