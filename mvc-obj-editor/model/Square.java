package model;

import java.io.FileInputStream;
import java.io.ObjectInputStream;

public class Square extends Shape {
	private static final long serialVersionUID = 1298462627245771577L;

	private double side;

	public Square() {
		super(0.0, 0.0, "Square");
		this.side = 0.0;
	}

	public Square(double x, double y, double side) throws Exception {
		super(x, y, "Square");
		if (side >= 0) this.side = side;
		else throw new Exception("Side must be nonnegative.");
	}

	public double getSide() {
		return side;
	}

	public void setSide(double val) throws Exception {
		if (val >= 0) side = val;
		else throw new Exception("Side must be nonnegative.");
	}

	@Override
	public String toString() {
		return super.toString() + ", side: " + side + ".";
	}

	public static Square fromFile(String filePath) {
		try {
			FileInputStream fis = new FileInputStream(filePath);
			ObjectInputStream ois = new ObjectInputStream(fis);
			
			Square input = (Square) ois.readObject();

			fis.close();
			ois.close();

			input.setFilePath(filePath);
			return input;
		} catch (Exception e) {
			return null;
		}
	}
}
