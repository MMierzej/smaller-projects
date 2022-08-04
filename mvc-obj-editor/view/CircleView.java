package view;

import javax.swing.*;

public class CircleView extends ShapeView {
	public CircleView() {
		super(new JLabel("radius:"), new JTextField(15));
	}
}
