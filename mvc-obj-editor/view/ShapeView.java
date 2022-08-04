package view;

import java.awt.*;

import javax.swing.*;

import controller.ShapeController;

public abstract class ShapeView extends JPanel {
	private ShapeController controller;

	private JLabel header;
	private JLabel info;
	private JLabel xLabel;
	private JTextField xField;
	private JLabel yLabel;
	private JTextField yField;
	private JLabel paramLabel;
	private JTextField paramField;
	private JButton save;

	public ShapeView(JLabel pl, JTextField pf) {
		header = new JLabel("Shape Editor");
		header.setHorizontalAlignment(JLabel.CENTER);

		info = new JLabel();
		info.setHorizontalAlignment(JLabel.CENTER);

		xLabel = new JLabel("x:");
		xLabel.setHorizontalAlignment(JLabel.CENTER);
		xField = new JTextField(15);

		yLabel = new JLabel("y:");
		yLabel.setHorizontalAlignment(JLabel.CENTER);
		yField = new JTextField(15);

		paramLabel = pl;
		paramField = pf;

		save = new JButton("Save");


		this.setLayout(new GridBagLayout());
		GridBagConstraints gbc = new GridBagConstraints();
		gbc.insets = new Insets(5, 5, 5, 5);

		gbc.gridx = 0;
		gbc.gridy = 0;
		gbc.gridwidth = 2;
		this.add(header, gbc);

		gbc.gridx = 0;
		gbc.gridy = 1;
		this.add(info, gbc);
		gbc.gridwidth = 1;

		gbc.gridx = 0;
		gbc.gridy = 2;
		this.add(xLabel, gbc);

		gbc.gridx = 1;
		gbc.gridy = 2;
		this.add(xField, gbc);

		gbc.gridx = 0;
		gbc.gridy = 3;
		this.add(yLabel, gbc);

		gbc.gridx = 1;
		gbc.gridy = 3;
		this.add(yField, gbc);

		gbc.gridx = 0;
		gbc.gridy = 4;
		this.add(paramLabel, gbc);

		gbc.gridx = 1;
		gbc.gridy = 4;
		this.add(paramField, gbc);

		gbc.gridx = 0;
		gbc.gridy = 5;
		gbc.gridwidth = 2;
		this.add(save, gbc);
	}

	public double getXValue() {
		return Double.parseDouble(xField.getText());
	}

	public double getYValue() {
		return Double.parseDouble(yField.getText());
	}
	
	public double getParamValue() {
		return Double.parseDouble(paramField.getText());
	}

	public void update() {
		info.setText(controller.getInfo());
	}

	public void errorMsg(String msg) {
		JOptionPane.showMessageDialog(this, msg);
	}

	public void addController(ShapeController controller) {
		this.controller = controller;
		save.addActionListener(controller);
		update();
	}
}
