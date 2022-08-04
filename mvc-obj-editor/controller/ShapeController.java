package controller;

import java.awt.event.*;

import model.Shape;
import view.ShapeView;

public class ShapeController implements ActionListener {
	protected Shape shape;
	protected ShapeView view;

	public ShapeController(Shape shape, ShapeView view) {
		this.shape = shape;
		this.view = view;
		view.addController(this);
	}

	public String getInfo() {
		return shape.toString();
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		try {
			shape.moveX(view.getXValue());
			shape.moveY(view.getYValue());
			view.update();
		} catch (Exception exc) {
			view.errorMsg("Wrong input!");
		}
	}
}