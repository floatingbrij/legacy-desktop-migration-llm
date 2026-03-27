using System;
using System.Windows.Forms;

namespace SimpleCalc
{
    public partial class CalculatorForm : Form
    {
        private double currentValue = 0;
        private string currentOperator = "";
        private bool newNumber = true;

        public CalculatorForm()
        {
            InitializeComponent();
        }

        private void btnNumber_Click(object sender, EventArgs e)
        {
            Button btn = (Button)sender;
            if (newNumber)
            {
                txtDisplay.Text = btn.Text;
                newNumber = false;
            }
            else
            {
                txtDisplay.Text += btn.Text;
            }
        }

        private void btnOperator_Click(object sender, EventArgs e)
        {
            Button btn = (Button)sender;
            currentValue = double.Parse(txtDisplay.Text);
            currentOperator = btn.Text;
            newNumber = true;
            lblResult.Text = $"{currentValue} {currentOperator}";
        }

        private void btnEquals_Click(object sender, EventArgs e)
        {
            double secondValue = double.Parse(txtDisplay.Text);
            double result = 0;
            switch (currentOperator)
            {
                case "+": result = currentValue + secondValue; break;
                case "-": result = currentValue - secondValue; break;
                case "*": result = currentValue * secondValue; break;
                case "/":
                    if (secondValue != 0)
                        result = currentValue / secondValue;
                    else
                        MessageBox.Show("Cannot divide by zero!");
                    break;
            }
            txtDisplay.Text = result.ToString();
            lblResult.Text = "";
            newNumber = true;
        }

        private void btnClear_Click(object sender, EventArgs e)
        {
            txtDisplay.Text = "0";
            lblResult.Text = "";
            currentValue = 0;
            currentOperator = "";
            newNumber = true;
        }
    }
}
