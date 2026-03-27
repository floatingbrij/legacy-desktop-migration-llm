using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace SimpleCalc
{
    public partial class CalculatorFormViewModel : ObservableObject
    {
        [RelayCommand]
        private void btnNumber()
        {
            Button btn = ;
            if (newNumber)
            {
            txtDisplayText = btnText;
            newNumber = false;
            }
            else
            {
            txtDisplayText += btnText;
            }
        }

        [RelayCommand]
        private void btnOperator()
        {
            Button btn = ;
            currentValue = double.Parse(txtDisplayText);
            currentOperator = btnText;
            newNumber = true;
            lblResultText = $"{currentValue} {currentOperator}";
        }

        [RelayCommand]
        private async Task btnEqualsAsync()
        {
            double secondValue = double.Parse(txtDisplayText);
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
            txtDisplayText = result.ToString();
            lblResultText = "";
            newNumber = true;
        }

        [RelayCommand]
        private void btnClear()
        {
            txtDisplayText = "0";
            lblResultText = "";
            currentValue = 0;
            currentOperator = "";
            newNumber = true;
        }

    }
}