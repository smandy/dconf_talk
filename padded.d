template Padded(T) {
  const postAmbleLength = 128 - 4 * long.sizeof - T.sizeof;
  struct Padded {
	 private long[4] preamble;
	 T value;
	 private byte[postAmbleLength] postAmble;

	 alias value this;
  };
};
