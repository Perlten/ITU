package readWriterProblem;

public class MonitorImpl {

    private int readLockAcquired = 0;
    private int readLockRelased = 0;

    private boolean write = false;

    public synchronized void lockRead() {
        while (write) {
            try {
                this.wait();
            } catch (InterruptedException e) {
            }
        }
        readLockAcquired++;
    }

    public synchronized void releaseLockRead() {
        readLockRelased++;
        if (readLockAcquired == readLockRelased) {
            this.notifyAll();
        }
    }

    public synchronized void lockWrite() {
        try {
            while (write) {
                this.wait();
            }

            write = true;

            while (readLockAcquired != readLockRelased) {
                this.wait();
            }
        } catch (InterruptedException e) {
        }
    }

    public synchronized void releaseLockWrite() {
        write = false;
        this.notifyAll();
    }

}