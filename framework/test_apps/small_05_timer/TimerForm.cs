using System;
using System.Windows.Forms;
using System.Drawing;

namespace TimerApp
{
    public partial class TimerForm : Form
    {
        public TimerForm()
        {
            InitializeComponent();
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            timer1.Start();
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            timer1.Stop();
        }

        private void btnReset_Click(object sender, EventArgs e)
        {
            timer1.Stop(); lblTime.Text = "00:00:00";
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            TimeSpan ts = DateTime.Now - startTime;
            lblTime.Text = ts.ToString(@"hh\:mm\:ss");
        }
    }
}