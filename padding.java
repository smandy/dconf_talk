/**
 * Pad out a cacheline to the left of a tail to prevent false sharing.
 */
class Padding1
{
    @SuppressWarnings("unused")
    protected long p1, p2, p3, p4, p5, p6, p7;
}

/**
 * Value for the tail that is expected to be padded.
 */
class Tail extends Padding1
{
    protected volatile long tail;
}

/**
 * Pad out a cacheline between the tail and the head to prevent false sharing.
 */
class Padding2 extends Tail
{
    @SuppressWarnings("unused")
    protected long p8, p9, p10, p11, p12, p13, p14;
}

/**
 * Value for the head that is expected to be padded.
 */
class Head extends Padding2
{
    protected volatile long head;
}
