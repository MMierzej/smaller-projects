import javax.swing.*;

public class Window extends JFrame {
	public Window(JPanel panel) {
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setSize(350, 250);
		this.add(panel);
		this.setVisible(true);
	}
}
