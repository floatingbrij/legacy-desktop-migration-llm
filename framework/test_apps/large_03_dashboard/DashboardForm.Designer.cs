namespace DashboardApp
{
    partial class DashboardForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.panelTop = new System.Windows.Forms.Panel();
            this.panelLeft = new System.Windows.Forms.Panel();
            this.panelMain = new System.Windows.Forms.Panel();
            this.lblWelcome = new System.Windows.Forms.Label();
            this.lblDate = new System.Windows.Forms.Label();
            this.btnDashboard = new System.Windows.Forms.Button();
            this.btnReports = new System.Windows.Forms.Button();
            this.btnUsers = new System.Windows.Forms.Button();
            this.btnSettings = new System.Windows.Forms.Button();
            this.btnLogout = new System.Windows.Forms.Button();
            this.dgvData = new System.Windows.Forms.DataGridView();
            this.picChart = new System.Windows.Forms.PictureBox();
            this.panelStats = new System.Windows.Forms.Panel();
            this.lblStat1 = new System.Windows.Forms.Label();
            this.lblStat2 = new System.Windows.Forms.Label();
            this.lblStat3 = new System.Windows.Forms.Label();
            this.lblStat4 = new System.Windows.Forms.Label();
            this.dtpStart = new System.Windows.Forms.DateTimePicker();
            this.dtpEnd = new System.Windows.Forms.DateTimePicker();
            this.btnRefresh = new System.Windows.Forms.Button();
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.refreshTimer = new System.Windows.Forms.Timer();
            this.cmbView = new System.Windows.Forms.ComboBox();
            this.chkAutoRefresh = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // menuStrip1
            this.menuStrip1.Name = "menuStrip1";
            // panelTop
            this.panelTop.Size = new System.Drawing.Size(1200, 80);
            this.panelTop.Dock = DockStyle.Top;
            this.panelTop.Name = "panelTop";
            // panelLeft
            this.panelLeft.Size = new System.Drawing.Size(250, 720);
            this.panelLeft.Dock = DockStyle.Left;
            this.panelLeft.Name = "panelLeft";
            // panelMain
            this.panelMain.Dock = DockStyle.Fill;
            this.panelMain.Name = "panelMain";
            // lblWelcome
            this.lblWelcome.Text = "Welcome, User";
            this.lblWelcome.Location = new System.Drawing.Point(20, 20);
            this.lblWelcome.Size = new System.Drawing.Size(300, 40);
            this.lblWelcome.Font = new System.Drawing.Font("Segoe UI", 18F);
            this.lblWelcome.Name = "lblWelcome";
            // lblDate
            this.lblDate.Text = "March 28, 2026";
            this.lblDate.Location = new System.Drawing.Point(20, 55);
            this.lblDate.Size = new System.Drawing.Size(200, 20);
            this.lblDate.Name = "lblDate";
            // btnDashboard
            this.btnDashboard.Text = "Dashboard";
            this.btnDashboard.Location = new System.Drawing.Point(10, 10);
            this.btnDashboard.Size = new System.Drawing.Size(230, 35);
            this.btnDashboard.Name = "btnDashboard";
            this.btnDashboard.Click += new System.EventHandler(this.btnDashboard_Click);
            // btnReports
            this.btnReports.Text = "Reports";
            this.btnReports.Location = new System.Drawing.Point(10, 50);
            this.btnReports.Size = new System.Drawing.Size(230, 35);
            this.btnReports.Name = "btnReports";
            this.btnReports.Click += new System.EventHandler(this.btnReports_Click);
            // btnUsers
            this.btnUsers.Text = "Users";
            this.btnUsers.Location = new System.Drawing.Point(10, 90);
            this.btnUsers.Size = new System.Drawing.Size(230, 35);
            this.btnUsers.Name = "btnUsers";
            this.btnUsers.Click += new System.EventHandler(this.btnUsers_Click);
            // btnSettings
            this.btnSettings.Text = "Settings";
            this.btnSettings.Location = new System.Drawing.Point(10, 130);
            this.btnSettings.Size = new System.Drawing.Size(230, 35);
            this.btnSettings.Name = "btnSettings";
            this.btnSettings.Click += new System.EventHandler(this.btnSettings_Click);
            // btnLogout
            this.btnLogout.Text = "Logout";
            this.btnLogout.Location = new System.Drawing.Point(10, 650);
            this.btnLogout.Size = new System.Drawing.Size(230, 35);
            this.btnLogout.Name = "btnLogout";
            this.btnLogout.Click += new System.EventHandler(this.btnLogout_Click);
            // dgvData
            this.dgvData.Location = new System.Drawing.Point(10, 10);
            this.dgvData.Size = new System.Drawing.Size(700, 400);
            this.dgvData.Name = "dgvData";
            this.dgvData.CellClick += new System.EventHandler(this.dgvData_CellClick);
            // picChart
            this.picChart.Location = new System.Drawing.Point(10, 420);
            this.picChart.Size = new System.Drawing.Size(700, 250);
            this.picChart.Name = "picChart";
            // panelStats
            this.panelStats.Location = new System.Drawing.Point(720, 10);
            this.panelStats.Size = new System.Drawing.Size(220, 660);
            this.panelStats.Name = "panelStats";
            // lblStat1
            this.lblStat1.Text = "Total Users: 0";
            this.lblStat1.Location = new System.Drawing.Point(10, 10);
            this.lblStat1.Size = new System.Drawing.Size(200, 25);
            this.lblStat1.Name = "lblStat1";
            // lblStat2
            this.lblStat2.Text = "Revenue: $0";
            this.lblStat2.Location = new System.Drawing.Point(10, 40);
            this.lblStat2.Size = new System.Drawing.Size(200, 25);
            this.lblStat2.Name = "lblStat2";
            // lblStat3
            this.lblStat3.Text = "Orders: 0";
            this.lblStat3.Location = new System.Drawing.Point(10, 70);
            this.lblStat3.Size = new System.Drawing.Size(200, 25);
            this.lblStat3.Name = "lblStat3";
            // lblStat4
            this.lblStat4.Text = "Pending: 0";
            this.lblStat4.Location = new System.Drawing.Point(10, 100);
            this.lblStat4.Size = new System.Drawing.Size(200, 25);
            this.lblStat4.Name = "lblStat4";
            // dtpStart
            this.dtpStart.Location = new System.Drawing.Point(10, 140);
            this.dtpStart.Size = new System.Drawing.Size(200, 23);
            this.dtpStart.Name = "dtpStart";
            this.dtpStart.ValueChanged += new System.EventHandler(this.dtpStart_Changed);
            // dtpEnd
            this.dtpEnd.Location = new System.Drawing.Point(10, 170);
            this.dtpEnd.Size = new System.Drawing.Size(200, 23);
            this.dtpEnd.Name = "dtpEnd";
            this.dtpEnd.ValueChanged += new System.EventHandler(this.dtpEnd_Changed);
            // btnRefresh
            this.btnRefresh.Text = "Refresh";
            this.btnRefresh.Location = new System.Drawing.Point(10, 200);
            this.btnRefresh.Size = new System.Drawing.Size(200, 30);
            this.btnRefresh.Name = "btnRefresh";
            this.btnRefresh.Click += new System.EventHandler(this.btnRefresh_Click);
            // progressBar1
            this.progressBar1.Location = new System.Drawing.Point(10, 640);
            this.progressBar1.Size = new System.Drawing.Size(200, 20);
            this.progressBar1.Name = "progressBar1";
            // refreshTimer
            this.refreshTimer.Name = "refreshTimer";
            this.refreshTimer.Tick += new System.EventHandler(this.refreshTimer_Tick);
            // cmbView
            this.cmbView.Location = new System.Drawing.Point(10, 240);
            this.cmbView.Size = new System.Drawing.Size(200, 23);
            this.cmbView.Name = "cmbView";
            this.cmbView.SelectedIndexChanged += new System.EventHandler(this.cmbView_Changed);
            // chkAutoRefresh
            this.chkAutoRefresh.Text = "Auto-refresh";
            this.chkAutoRefresh.Location = new System.Drawing.Point(10, 270);
            this.chkAutoRefresh.Size = new System.Drawing.Size(200, 20);
            this.chkAutoRefresh.Name = "chkAutoRefresh";
            this.chkAutoRefresh.CheckedChanged += new System.EventHandler(this.chkAutoRefresh_Changed);
            // DashboardForm
            this.ClientSize = new System.Drawing.Size(1200, 800);
            this.Controls.Add(this.chkAutoRefresh);
            this.Controls.Add(this.cmbView);
            this.Controls.Add(this.progressBar1);
            this.Controls.Add(this.btnRefresh);
            this.Controls.Add(this.dtpEnd);
            this.Controls.Add(this.dtpStart);
            this.Controls.Add(this.lblStat4);
            this.Controls.Add(this.lblStat3);
            this.Controls.Add(this.lblStat2);
            this.Controls.Add(this.lblStat1);
            this.Controls.Add(this.panelStats);
            this.Controls.Add(this.picChart);
            this.Controls.Add(this.dgvData);
            this.Controls.Add(this.btnLogout);
            this.Controls.Add(this.btnSettings);
            this.Controls.Add(this.btnUsers);
            this.Controls.Add(this.btnReports);
            this.Controls.Add(this.btnDashboard);
            this.Controls.Add(this.lblDate);
            this.Controls.Add(this.lblWelcome);
            this.Controls.Add(this.panelMain);
            this.Controls.Add(this.panelLeft);
            this.Controls.Add(this.panelTop);
            this.Controls.Add(this.menuStrip1);
            this.Name = "DashboardForm";
            this.Text = "Dashboard";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.Panel panelTop;
        private System.Windows.Forms.Panel panelLeft;
        private System.Windows.Forms.Panel panelMain;
        private System.Windows.Forms.Label lblWelcome;
        private System.Windows.Forms.Label lblDate;
        private System.Windows.Forms.Button btnDashboard;
        private System.Windows.Forms.Button btnReports;
        private System.Windows.Forms.Button btnUsers;
        private System.Windows.Forms.Button btnSettings;
        private System.Windows.Forms.Button btnLogout;
        private System.Windows.Forms.DataGridView dgvData;
        private System.Windows.Forms.PictureBox picChart;
        private System.Windows.Forms.Panel panelStats;
        private System.Windows.Forms.Label lblStat1;
        private System.Windows.Forms.Label lblStat2;
        private System.Windows.Forms.Label lblStat3;
        private System.Windows.Forms.Label lblStat4;
        private System.Windows.Forms.DateTimePicker dtpStart;
        private System.Windows.Forms.DateTimePicker dtpEnd;
        private System.Windows.Forms.Button btnRefresh;
        private System.Windows.Forms.ProgressBar progressBar1;
        private System.Windows.Forms.Timer refreshTimer;
        private System.Windows.Forms.ComboBox cmbView;
        private System.Windows.Forms.CheckBox chkAutoRefresh;
    }
}