using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace SimpleCalc
{
    public sealed partial class CalculatorForm : Window
    {
        public CalculatorForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void btnNumber_Click(object sender, RoutedEventArgs e)
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

        // Migrated from WinForms event handler
        private void btnOperator_Click(object sender, RoutedEventArgs e)
        {
            Button btn = (Button)sender;
                        currentValue = double.Parse(txtDisplay.Text);
                        currentOperator = btn.Text;
                        newNumber = true;
                        lblResult.Text = $"{currentValue} {currentOperator}";
        }

        // Migrated from WinForms event handler
        private void btnEquals_Click(object sender, RoutedEventArgs e)
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
                                    await ShowDialogAsync("Cannot divide by zero!");
                                break;
                        }
                        txtDisplay.Text = result.ToString();
                        lblResult.Text = "";
                        newNumber = true;
        }

        // Migrated from WinForms event handler
        private void btnClear_Click(object sender, RoutedEventArgs e)
        {
            txtDisplay.Text = "0";
                        lblResult.Text = "";
                        currentValue = 0;
                        currentOperator = "";
                        newNumber = true;
        }
    }
}