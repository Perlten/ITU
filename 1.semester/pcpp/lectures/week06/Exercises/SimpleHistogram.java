// For week 3
// sestoft@itu.dk * 2014-09-04
// thdy@itu.dk * 2019
// kasper@itu.dk * 2020

interface Histogram {
  public void increment(int bin);
  public int getCount(int bin);
  public float getPercentage(int bin);
  public int getSpan();
  public int getTotal();
}

public class SimpleHistogram {
  public static void main(String[] args) {
    final Histogram histogram = new Histogram1(30);
    histogram.increment(7);
    histogram.increment(13);
    histogram.increment(7);
    dump(histogram);
}

  public static void dump(Histogram histogram) {
    for (int bin = 0; bin < histogram.getSpan(); bin++) {
      System.out.printf("%4d: %9d%n", bin, histogram.getCount(bin));
    }
    System.out.printf("      %9d%n", histogram.getTotal() );
  }
}

class Histogram1 implements Histogram {
  private int[] counts;
  private int total=0;

  public Histogram1(int span) {
    this.counts = new int[span];
  }

  public void increment(int bin) {
    counts[bin] = counts[bin] + 1;
    total++;
  }

  public int getCount(int bin) {
    return counts[bin];
  }
    
  public float getPercentage(int bin){
    return getCount(bin) / getTotal() * 100;
  }

  public int getSpan() {
    return counts.length;
  }
    
  public int getTotal(){
    return total;
  }
}


