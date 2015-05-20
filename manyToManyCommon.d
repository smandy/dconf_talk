shared struct Header(T, int Consumers, int Capacity) {
  Padded!long            reserveTail;
  Padded!long            commitTail;
  Padded!long[Consumers] heads;
};

mixin template ManyToManyCommon(T, 
										  int Consumers, 
										  int Capacity, 
										  int IDX = 1 ) if (IDX<=Consumers) {
  alias Header!(T, Consumers, Capacity) HeaderType;

  mixin QueueCommon!();

  HeaderType* header;
  T* data;

  mixin MultipleHeads;

  final long getTail() {
	 return atomicLoad!(MemoryOrder.acq)( header.commitTail.value);
  };

};



