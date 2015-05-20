bool delegate (int) olderThan( int n ) {
  return delegate bool(int x) {
    return x > n;
  };
}
