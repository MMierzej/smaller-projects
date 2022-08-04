import model.*;
import view.*;
import controller.*;

public class Main {
	public static final String cliErrMsg = """
			\n\t\tInvalid command line arguments.
			\t\t1st arg: name of the file containing the shape.
			\t\t2nd arg: shape's type: Circle/Square.""";

	public static void main(String[] args) throws Exception {
		if (args.length != 2) throw new Exception(cliErrMsg);

		Shape shape;
		ShapeView view;

		if (args[1].equals("Circle")) {
			shape = Circle.fromFile(args[0]);
			if (shape == null) {
				shape = new Circle();
				shape.setFilePath(args[0]);
			}
			view = new CircleView();
			new CircleController((Circle) shape, (CircleView) view);
		} else if (args[1].equals("Square")) {
			shape = Square.fromFile(args[0]);
			if (shape == null) {
				shape = new Square();
				shape.setFilePath(args[0]);
			}
			view = new SquareView();
			new SquareController((Square) shape, (SquareView) view);
		} else throw new Exception(cliErrMsg);

		new Window(view);
	}
}
