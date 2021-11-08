// For week 7
// raup@itu.dk * 10/10/2021
package exercises07;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

class ReadWriteCASLock implements SimpleRWTryLockInterface {

    public static void main(String[] args) {
        // TODO execute tests (7.2.5 & 7.2.6)
    }

    private AtomicReference<ReadWriteCASLock.Holders> holder;

    public boolean readerTryLock() {

        var currentHolder = this.holder;
        if (currentHolder == null || currentHolder.get() instanceof ReaderList) {
            var currentReaderList = (ReaderList) currentHolder.get();
            var latestReaderList = currentReaderList;

            while (latestReaderList.next != null) {
                latestReaderList = latestReaderList.next;
            }

            latestReaderList.next = new ReaderList(Thread.currentThread(), latestReaderList);

            return this.holder.compareAndSet(currentReaderList, currentReaderList);
        }
        return false;
    }

    public void readerUnlock() throws Exception {
        var currentThread = Thread.currentThread();
        var currentHolder = this.holder.get();

        if (currentHolder == null || currentHolder instanceof Writer) {
            throw new Exception("YOU ARE NOT THE HOLDER !!");
        }

        var currentReader = (ReaderList) this.holder.get();
        if (currentReader.thread == currentThread) {
            currentReader = currentReader.next;
        } else {

            var latestReader = currentReader;
            do {
                if (latestReader.thread == currentThread) {
                    latestReader.parrent.next = latestReader.next;
                    break;
                }
                latestReader = latestReader.next;
            } while (latestReader != null);
        }
        this.holder.compareAndSet(currentReader, currentReader);
    }

    public boolean writerTryLock() {
        Holders newHolder = new Writer(Thread.currentThread());
        return this.holder.compareAndSet(null, newHolder);
    }

    public void writerUnlock() throws Exception {
        var currentHolder = this.holder.get();
        if (currentHolder instanceof Writer) {
            Writer writer = (Writer) currentHolder;
            if (writer.thread != Thread.currentThread()) {
                throw new Exception("YOU ARE NOT THE HOLDER !!");
            }
            this.holder.compareAndSet(currentHolder, null);
        }

    }

    private static abstract class Holders {
    }

    private static class ReaderList extends Holders {
        private final Thread thread;
        private ReaderList next = null;
        private ReaderList parrent = null;

        public ReaderList(Thread t, ReaderList parrent) {
            this.thread = t;
            this.parrent = parrent;
        }

        // TODO: contains

        // TODO: remove
    }

    private static class Writer extends Holders {
        public final Thread thread;

        public Writer(Thread t) {
            this.thread = t;
        }

    }
}
