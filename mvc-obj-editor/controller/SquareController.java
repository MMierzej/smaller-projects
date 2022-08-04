package controller;

import java.awt.event.*;

import model.Square;
import view.SquareView;

public class SquareController extends ShapeController {
	private Square square;

	public SquareController(Square square, SquareView view) {
		super(square, view);
		this.square = square;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		try {
			square.setSide(view.getParamValue());
		} catch (Exception exc) {
			view.errorMsg("Wrong input!");
		}
		super.actionPerformed(e);
		square.toFile(square.getFilePath());
	}
}
