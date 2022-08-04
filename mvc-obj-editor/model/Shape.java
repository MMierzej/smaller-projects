package model;

import java.io.Serializable;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;

public abstract class Shape implements Serializable {
	private static final long serialVersionUID = 7198768692654876314L;

	protected static long idCount = 0;

	private String type;
	private long id;

	// center-of-mass coordinates
	private double x;
	private double y;

	protected String filePath;

	public Shape(double x, double y, String type) {
		this.x = x;
		this.y = y;
		this.type = type;
		id = idCount++;
	}

	public String toString() {
		return type + " " + id + " at (" + x +", " + y + ")";
	}

	public void moveX(double x) {
		this.x = x;
	}

	public void moveY(double y) {
		this.y = y;
	}

	public double getX() {
		return x;
	}

	public double getY() {
		return y;
	}

	public boolean toFile(String filePath) {
		try {
			FileOutputStream fos = new FileOutputStream(filePath);
			ObjectOutputStream oos = new ObjectOutputStream(fos);
			
			oos.writeObject(this);

			fos.close();
			oos.close();

			return true;
		} catch (Exception e) {
			return false;
		}
	}

	public void setFilePath(String filePath) {
		this.filePath = filePath;
	}

	public String getFilePath() {
		return filePath;
	}
}