// For week 5
// raup@itu.dk * 26/09/2021
package lecture05;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.util.ConcurrentModificationException;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.stream.IntStream;

class LiveCodingStreams {
    public static void main(String[] args) {

	// Creating streams
	String[] stringArray = {"e1","e2","e3"};
	Arrays.stream(stringArray).forEach(System.out::println); // using Arrays
	Arrays.asList("e1","e2","e3").stream().forEach(System.out::println); // using stream() in collection	
	IntStream.iterate(0,x->x+1).limit(10).forEach(System.out::println); // Infinite stream | what happens if I remove `limit(10)`?

	// Map over infinite stream
	IntStream.iterate(0,x->x+1).map(x->x+2); // Adds two to the infinite set of natural numbers (including 0)


	// reduce
	System.out.println( IntStream.range(0,100).reduce(0, (a,b) -> a+b*b) );
	System.out.println( IntStream.range(0,100).reduce((a,b) -> a+b*b).orElse(0) );

	// number of even numbers in the 100 naturals
	int numEvenNaturals = IntStream.iterate(0,x->x+1)
	    .limit(100)
	    .filter(x -> x%2==0)
	    .map(x -> 1)
	    .reduce(0, (a,b) -> a+b);
	System.out.println(numEvenNaturals);

	// Parallel Streams
	IntStream.range(0,10).parallel().forEach(System.out::println); // Note the priting order
	IntStream.range(0,10).parallel().forEachOrdered(System.out::println);


	// Interfering streams (concurrent modification exception)
	List<String> list = new ArrayList<String>();
	list.add("a");
	list.add("b");
	list.add("c");
	try {
	    // don't do this!
	    list.stream().forEach(e -> list.add(e));	    
	}
	catch (ConcurrentModificationException e) {
	    e.printStackTrace();
	}	
    }

    
}
