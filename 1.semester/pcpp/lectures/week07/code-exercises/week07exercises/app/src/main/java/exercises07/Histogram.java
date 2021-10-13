package exercises07;


public interface Histogram {
    public void increment(int bin);

    public int getCount(int bin);

    public int getSpan();

    public int getAndClear(int bin);

    // Not thread safe only for debugging
    public void print();
}