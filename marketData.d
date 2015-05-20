align(1) struct BidAskChange {
  int    messageType;     
  int    securityId;
  long   timeStamp;
  long   bidQty;
  double bidPrice;
  long   askQty;
  double askPrice;
};

pragma(msg, "Size is ", BidAskChange.sizeof);
static assert (BidAskChange.sizeof == 48);
