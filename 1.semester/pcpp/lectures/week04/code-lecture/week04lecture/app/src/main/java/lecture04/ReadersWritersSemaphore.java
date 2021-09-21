// For week 2
// raup@itu.dk * 01/09/2021
package lecture04;

import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicInteger;

public class ReadersWritersSemaphore {

    public ReadersWritersSemaphore() {

	FairReadWriteMonitor m  = new FairReadWriteMonitor();
	Semaphore semReaders    = new Semaphore(5,true);
	Semaphore semWriters    = new Semaphore(5,true);
	AtomicInteger noReaders = new AtomicInteger(0);
	AtomicInteger noWriters = new AtomicInteger(0);

	final int numReadersWriters = 10;

	for (int i = 0; i < numReadersWriters; i++) {

	    // start a reader
	    new Thread(() -> {
		    try{semReaders.acquire();}catch(InterruptedException e){e.printStackTrace();System.exit(-1);}
		    m.readLock();
		    // Note that it always prints less than 5 readers (do not mind the printing order)
		    System.out.println("There are " + noReaders.incrementAndGet() + " readers ready to read");
		    // read
		    m.readUnlock();
		    noReaders.decrementAndGet();
		    semReaders.release();
	    }).start();

	    // start a writer
	    new Thread(() -> {
		    try{semWriters.acquire();}catch(InterruptedException e){e.printStackTrace();System.exit(-1);}
		    // Note that it always prints less than 5 writers (do not mind the printing order)
		    System.out.println("There are " + noWriters.incrementAndGet() + " writers ready to write");
		    m.writeLock();
		    // write
		    m.writeUnlock();
		    noWriters.decrementAndGet();
		    semWriters.release();
	    }).start();
	    
	}
    }

    public static void main(String[] args) {
	new ReadersWritersSemaphore();
    }
    
}
