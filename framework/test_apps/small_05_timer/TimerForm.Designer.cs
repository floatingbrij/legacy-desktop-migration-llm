namespace TimerApp
{
    partial class TimerForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.lblTime = new System.Windows.Forms.Label();
            this.btnStart = new System.Windows.Forms.Button();
            this.btnStop = new System.Windows.Forms.Button();
            this.btnReset = new System.Windows.Forms.Button();
            this.timer1 = new System.Windows.Forms.Timer();
            this.SuspendLayout();
            // lblTime
            this.lblTime.Text = "00:00:00";
            this.lblTime.Location = new System.Drawing.Point(40, 20);
            this.lblTime.Size = new System.Drawing.Size(200, 50);
            this.lblTime.Font = new System.Drawing.Font("Segoe UI", 24F);
            this.lblTime.Name = "lblTime";
            // btnStart
            this.btnStart.Text = "Start";
            this.btnStart.Location = new System.Drawing.Point(20, 90);
            this.btnStart.Size = new System.Drawing.Size(75, 30);
            this.btnStart.Name = "btnStart";
            this.btnStart.Click += new System.EventHandler(this.btnStart_Click);
            // btnStop
            this.btnStop.Text = "Stop";
            this.btnStop.Location = new System.Drawing.Point(100, 90);
            this.btnStop.Size = new System.Drawing.Size(75, 30);
            this.btnStop.Name = "btnStop";
            this.btnStop.Click += new System.EventHandler(this.btnStop_Click);
            // btnReset
            this.btnReset.Text = "Reset";
            this.btnReset.Location = new System.Drawing.Point(180, 90);
            this.btnReset.Size = new System.Drawing.Size(75, 30);
            this.btnReset.Name = "btnReset";
            this.btnReset.Click += new System.EventHandler(this.btnReset_Click);
            // timer1
            this.timer1.Name = "timer1";
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // TimerForm
            this.ClientSize = new System.Drawing.Size(280, 180);
            this.Controls.Add(this.btnReset);
            this.Controls.Add(this.btnStop);
            this.Controls.Add(this.btnStart);
            this.Controls.Add(this.lblTime);
            this.Name = "TimerForm";
            this.Text = "Timer";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Label lblTime;
        private System.Windows.Forms.Button btnStart;
        private System.Windows.Forms.Button btnStop;
        private System.Windows.Forms.Button btnReset;
        private System.Windows.Forms.Timer timer1;
    }
}