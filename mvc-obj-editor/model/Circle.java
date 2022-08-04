package model;

import java.io.FileInputStream;
import java.io.ObjectInputStream;

public class Circle extends Shape {
	private static final long serialVersionUID = 2398468791495867891L;

	private double radius;

	public Circle() {
		super(0.0, 0.0, "Circle");
		this.radius = 0.0;
	}

	public Circle(double x, double y, double radius) throws Exception {
		super(x, y, "Circle");
		if (radius >= 0) this.radius = radius;
		else throw new Exception("Radius must be nonnegative.");
	}

	public double getRadius() {
		return radius;
	}

	public void setRadius(double val) throws Exception {
		if (val >= 0) radius = val;
		else throw new Exception("Radius must be nonnegative.");
	}

	@Override
	public String toString() {
		return super.toString() + ", radius: " + radius + ".";
	}

	public static Circle fromFile(String filePath) {
		try {
			FileInputStream fis = new FileInputStream(filePath);
			ObjectInputStream ois = new ObjectInputStream(fis);
			
			Circle input = (Circle) ois.readObject();

			fis.close();
			ois.close();

			input.setFilePath(filePath);
			return input;
		} catch (Exception e) {
			return null;
		}
	}
}