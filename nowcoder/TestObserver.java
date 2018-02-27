package nowcoder;

import java.util.Vector;

/**
 * Created by Administrator on 2018/2/27.
 */

interface Observer {
    void update();
}

class Observer1 implements Observer {
    @Override
    public void update() {
        System.out.println("Observer1 update");
    }
}

class Observer2 implements Observer {
    @Override
    public void update() {
        System.out.println("Observer2 update");
    }
}

interface Subject {
    void add(Observer ob);

    void remove(Observer ob);

    void updateAll();

    void operator();
}

class AbstractSubject implements Subject {
    Vector<Observer> vectorOb = new Vector();

    @Override
    public void add(Observer ob) {
        vectorOb.add(ob);
    }

    @Override
    public void remove(Observer ob) {
        vectorOb.remove(ob);
    }

    @Override
    public void updateAll() {
        for (Observer ob : vectorOb) {
            ob.update();
        }
    }

    @Override
    public void operator() {

    }
}

class MySubject extends AbstractSubject {
    @Override
    public void operator() {
        System.out.println("operator");
        updateAll();
    }
}

public class TestObserver {

    public static void main(String[] args) {
        Observer ob1 = new Observer1();
        Observer ob2 = new Observer2();
        Subject subject = new MySubject();
        subject.add(ob1);
        subject.add(ob2);
        subject.operator();
    }
}
