package nowcoder;

/**
 * Created by Administrator on 2018/2/27.
 */
interface Sender {
    void send();
}

class MailSender implements Sender {
    @Override
    public void send() {
        System.out.println("send mail");
    }
}

class SMSSender implements Sender {
    @Override
    public void send() {
        System.out.println("send sms");
    }
}

class SimpleFactory {

    public Sender produce(String type) {
        Sender sender = null;
        if ("mail".equals(type)) {
            sender = new MailSender();

        } else if ("sms".equals(type)) {
            sender = new SMSSender();

        } else {
            System.out.println("type error");
        }
        return sender;
    }
}

class MultFactory {
    public Sender produceMail() {
        return new MailSender();
    }

    public Sender produceSms() {
        return new SMSSender();
    }
}

interface Produce{
    Sender produce();
}

class MailFactory implements Produce{
    @Override
    public Sender produce() {
        return new MailSender();
    }
}

class SMSFactory implements Produce{
    @Override
    public Sender produce() {
        return new SMSSender();
    }
}

public class TestFactory {

    public static void main(String[] args) {
//        SimpleFactory sf = new SimpleFactory();
//        Sender sender = sf.produce("sms");
//        sender.send();
//
//        MultFactory mf = new MultFactory();
//        Sender sender1 = mf.produceMail();
//        sender1.send();

        Produce produce = new MailFactory();
        Sender sender2 = produce.produce();
        sender2.send();
        Produce produce1 = new SMSFactory();
        Sender sender3 = produce1.produce();
        sender3.send();
    }
}



