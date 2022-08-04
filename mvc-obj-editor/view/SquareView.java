package view;

import javax.swing.*;

public class SquareView extends ShapeView {
	public SquareView() {
		super(new JLabel("side:"), new JTextField(15));
	}
}
