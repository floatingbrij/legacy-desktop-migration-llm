namespace SimpleCalc
{
    partial class CalculatorForm
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.txtDisplay = new System.Windows.Forms.TextBox();
            this.btn1 = new System.Windows.Forms.Button();
            this.btn2 = new System.Windows.Forms.Button();
            this.btn3 = new System.Windows.Forms.Button();
            this.btn4 = new System.Windows.Forms.Button();
            this.btn5 = new System.Windows.Forms.Button();
            this.btn6 = new System.Windows.Forms.Button();
            this.btn7 = new System.Windows.Forms.Button();
            this.btn8 = new System.Windows.Forms.Button();
            this.btn9 = new System.Windows.Forms.Button();
            this.btn0 = new System.Windows.Forms.Button();
            this.btnAdd = new System.Windows.Forms.Button();
            this.btnSubtract = new System.Windows.Forms.Button();
            this.btnMultiply = new System.Windows.Forms.Button();
            this.btnDivide = new System.Windows.Forms.Button();
            this.btnEquals = new System.Windows.Forms.Button();
            this.btnClear = new System.Windows.Forms.Button();
            this.lblResult = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // txtDisplay
            this.txtDisplay.Font = new System.Drawing.Font("Segoe UI", 18F);
            this.txtDisplay.Location = new System.Drawing.Point(12, 12);
            this.txtDisplay.Name = "txtDisplay";
            this.txtDisplay.ReadOnly = true;
            this.txtDisplay.Size = new System.Drawing.Size(260, 39);
            this.txtDisplay.Text = "0";
            this.txtDisplay.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // btn1
            this.btn1.Location = new System.Drawing.Point(12, 70);
            this.btn1.Name = "btn1";
            this.btn1.Size = new System.Drawing.Size(60, 50);
            this.btn1.Text = "1";
            this.btn1.Click += new System.EventHandler(this.btnNumber_Click);
            // btn2
            this.btn2.Location = new System.Drawing.Point(78, 70);
            this.btn2.Name = "btn2";
            this.btn2.Size = new System.Drawing.Size(60, 50);
            this.btn2.Text = "2";
            this.btn2.Click += new System.EventHandler(this.btnNumber_Click);
            // btn3
            this.btn3.Location = new System.Drawing.Point(144, 70);
            this.btn3.Name = "btn3";
            this.btn3.Size = new System.Drawing.Size(60, 50);
            this.btn3.Text = "3";
            this.btn3.Click += new System.EventHandler(this.btnNumber_Click);
            // btn4
            this.btn4.Location = new System.Drawing.Point(12, 126);
            this.btn4.Name = "btn4";
            this.btn4.Size = new System.Drawing.Size(60, 50);
            this.btn4.Text = "4";
            this.btn4.Click += new System.EventHandler(this.btnNumber_Click);
            // btn5
            this.btn5.Location = new System.Drawing.Point(78, 126);
            this.btn5.Name = "btn5";
            this.btn5.Size = new System.Drawing.Size(60, 50);
            this.btn5.Text = "5";
            this.btn5.Click += new System.EventHandler(this.btnNumber_Click);
            // btn6
            this.btn6.Location = new System.Drawing.Point(144, 126);
            this.btn6.Name = "btn6";
            this.btn6.Size = new System.Drawing.Size(60, 50);
            this.btn6.Text = "6";
            this.btn6.Click += new System.EventHandler(this.btnNumber_Click);
            // btn7
            this.btn7.Location = new System.Drawing.Point(12, 182);
            this.btn7.Name = "btn7";
            this.btn7.Size = new System.Drawing.Size(60, 50);
            this.btn7.Text = "7";
            this.btn7.Click += new System.EventHandler(this.btnNumber_Click);
            // btn8
            this.btn8.Location = new System.Drawing.Point(78, 182);
            this.btn8.Name = "btn8";
            this.btn8.Size = new System.Drawing.Size(60, 50);
            this.btn8.Text = "8";
            this.btn8.Click += new System.EventHandler(this.btnNumber_Click);
            // btn9
            this.btn9.Location = new System.Drawing.Point(144, 182);
            this.btn9.Name = "btn9";
            this.btn9.Size = new System.Drawing.Size(60, 50);
            this.btn9.Text = "9";
            this.btn9.Click += new System.EventHandler(this.btnNumber_Click);
            // btn0
            this.btn0.Location = new System.Drawing.Point(12, 238);
            this.btn0.Name = "btn0";
            this.btn0.Size = new System.Drawing.Size(126, 50);
            this.btn0.Text = "0";
            this.btn0.Click += new System.EventHandler(this.btnNumber_Click);
            // btnAdd
            this.btnAdd.Location = new System.Drawing.Point(210, 70);
            this.btnAdd.Name = "btnAdd";
            this.btnAdd.Size = new System.Drawing.Size(60, 50);
            this.btnAdd.Text = "+";
            this.btnAdd.Click += new System.EventHandler(this.btnOperator_Click);
            // btnSubtract
            this.btnSubtract.Location = new System.Drawing.Point(210, 126);
            this.btnSubtract.Name = "btnSubtract";
            this.btnSubtract.Size = new System.Drawing.Size(60, 50);
            this.btnSubtract.Text = "-";
            this.btnSubtract.Click += new System.EventHandler(this.btnOperator_Click);
            // btnMultiply
            this.btnMultiply.Location = new System.Drawing.Point(210, 182);
            this.btnMultiply.Name = "btnMultiply";
            this.btnMultiply.Size = new System.Drawing.Size(60, 50);
            this.btnMultiply.Text = "*";
            this.btnMultiply.Click += new System.EventHandler(this.btnOperator_Click);
            // btnDivide
            this.btnDivide.Location = new System.Drawing.Point(210, 238);
            this.btnDivide.Name = "btnDivide";
            this.btnDivide.Size = new System.Drawing.Size(60, 50);
            this.btnDivide.Text = "/";
            this.btnDivide.Click += new System.EventHandler(this.btnOperator_Click);
            // btnEquals
            this.btnEquals.Location = new System.Drawing.Point(144, 238);
            this.btnEquals.Name = "btnEquals";
            this.btnEquals.Size = new System.Drawing.Size(60, 50);
            this.btnEquals.Text = "=";
            this.btnEquals.Click += new System.EventHandler(this.btnEquals_Click);
            // btnClear
            this.btnClear.Location = new System.Drawing.Point(12, 294);
            this.btnClear.Name = "btnClear";
            this.btnClear.Size = new System.Drawing.Size(260, 40);
            this.btnClear.Text = "Clear";
            this.btnClear.Click += new System.EventHandler(this.btnClear_Click);
            // lblResult
            this.lblResult.Location = new System.Drawing.Point(12, 340);
            this.lblResult.Name = "lblResult";
            this.lblResult.Size = new System.Drawing.Size(260, 20);
            this.lblResult.Text = "";
            // CalculatorForm
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.ClientSize = new System.Drawing.Size(284, 371);
            this.Controls.Add(this.lblResult);
            this.Controls.Add(this.btnClear);
            this.Controls.Add(this.btnEquals);
            this.Controls.Add(this.btnDivide);
            this.Controls.Add(this.btnMultiply);
            this.Controls.Add(this.btnSubtract);
            this.Controls.Add(this.btnAdd);
            this.Controls.Add(this.btn0);
            this.Controls.Add(this.btn9);
            this.Controls.Add(this.btn8);
            this.Controls.Add(this.btn7);
            this.Controls.Add(this.btn6);
            this.Controls.Add(this.btn5);
            this.Controls.Add(this.btn4);
            this.Controls.Add(this.btn3);
            this.Controls.Add(this.btn2);
            this.Controls.Add(this.btn1);
            this.Controls.Add(this.txtDisplay);
            this.Name = "CalculatorForm";
            this.Text = "Calculator";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.TextBox txtDisplay;
        private System.Windows.Forms.Button btn1;
        private System.Windows.Forms.Button btn2;
        private System.Windows.Forms.Button btn3;
        private System.Windows.Forms.Button btn4;
        private System.Windows.Forms.Button btn5;
        private System.Windows.Forms.Button btn6;
        private System.Windows.Forms.Button btn7;
        private System.Windows.Forms.Button btn8;
        private System.Windows.Forms.Button btn9;
        private System.Windows.Forms.Button btn0;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.Button btnSubtract;
        private System.Windows.Forms.Button btnMultiply;
        private System.Windows.Forms.Button btnDivide;
        private System.Windows.Forms.Button btnEquals;
        private System.Windows.Forms.Button btnClear;
        private System.Windows.Forms.Label lblResult;
    }
}
