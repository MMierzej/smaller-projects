package controller;

import java.awt.event.*;

import model.Circle;
import view.CircleView;

public class CircleController extends ShapeController {
	private Circle circle;

	public CircleController(Circle circle, CircleView view) {
		super(circle, view);
		this.circle = circle;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		try {
			circle.setRadius(view.getParamValue());
		} catch (Exception exc) {
			view.errorMsg("Wrong input!");
		}
		super.actionPerformed(e);
		circle.toFile(circle.getFilePath());
	}
}
