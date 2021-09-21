package exercises04;

import java.util.LinkedList;
import java.util.concurrent.Semaphore;

public class BoundedBuffer<T> implements BoundedBufferInteface<T> {

    private LinkedList<T> buffer = new LinkedList<T>();
    private Semaphore semaphore = null;

    public BoundedBuffer(int bufferSize) {
        this.semaphore = new Semaphore(bufferSize);
    }

    @Override
    public T take() throws Exception {
        if (this.buffer.size() > 0) {
            T data = this.buffer.pop();
            try {
                System.out.println("take: " + data);
                this.semaphore.release();
            } finally {
                return data;
            }
        }
        return null;

    }

    @Override
    public void insert(T elem) throws Exception {
        this.semaphore.acquire();

        System.out.println("Insert: " + elem);
        this.buffer.add(elem);
    }

    public static void main(String[] args) throws Exception {
        BoundedBuffer<Integer> bb = new BoundedBuffer<>(10);

        for (int i = 0; i < 20; i++) {

            Thread 

            bb.insert(i);

            if (i % 2 == 0) {
                bb.take();
            }
        }

    }

}
