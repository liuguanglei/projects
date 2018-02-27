package nowcoder;

/**
 * Created by Administrator on 2018/2/27.
 */


class Source {
    public void method1() {
        System.out.println("Source method1");
    }
}

interface Targetable {
    void method1();

    void method2();
}

class Adapter extends Source implements Targetable {

    @Override
    public void method2() {
        System.out.println("adapter method2");
    }
}

public class TestAdapter {
    public static void main(String[] args) {
        Adapter adapter = new Adapter();
        adapter.method1();
        adapter.method2();
    }
}
