void dumpType(T, string member)() {
  auto val = T.init;
  auto sizeOf  = __traits(getMember, val, member).sizeof;
  auto alignOf = __traits(getMember, val, member).alignof;
  auto offsetOf = __traits(getMember, val, member).offsetof;
  auto stringof = typeof(__traits(getMember, val, member)).stringof;
  writefln("%20s %4s align=%s stringof=%7s offset=%s", 
           member, sizeOf, alignOf, stringof, offsetOf);
};
  
void dumpInfo(T)()  {
  foreach(member ; __traits(derivedMembers, T)) {
    dumpType!( T, member);
  }
};

void main() {

  dumpInfo!BidAskChange;
};