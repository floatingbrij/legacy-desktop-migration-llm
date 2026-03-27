namespace EmailClient
{
    partial class EmailForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.toolStrip1 = new System.Windows.Forms.ToolStrip();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.splitMain = new System.Windows.Forms.SplitContainer();
            this.tvFolders = new System.Windows.Forms.TreeView();
            this.lvEmails = new System.Windows.Forms.ListView();
            this.rtbBody = new System.Windows.Forms.RichTextBox();
            this.panelHeader = new System.Windows.Forms.Panel();
            this.lblFrom = new System.Windows.Forms.Label();
            this.lblFromValue = new System.Windows.Forms.Label();
            this.lblSubject = new System.Windows.Forms.Label();
            this.lblSubjectValue = new System.Windows.Forms.Label();
            this.lblDate = new System.Windows.Forms.Label();
            this.lblDateValue = new System.Windows.Forms.Label();
            this.btnCompose = new System.Windows.Forms.Button();
            this.btnReply = new System.Windows.Forms.Button();
            this.btnForward = new System.Windows.Forms.Button();
            this.btnDelete = new System.Windows.Forms.Button();
            this.btnRefresh = new System.Windows.Forms.Button();
            this.txtSearch = new System.Windows.Forms.TextBox();
            this.lblStatus = new System.Windows.Forms.Label();
            this.checkMailTimer = new System.Windows.Forms.Timer();
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.notifyIcon1 = new System.Windows.Forms.NotifyIcon();
            this.ctxMenu = new System.Windows.Forms.ContextMenuStrip();
            this.SuspendLayout();
            // menuStrip1
            this.menuStrip1.Name = "menuStrip1";
            // toolStrip1
            this.toolStrip1.Name = "toolStrip1";
            // statusStrip1
            this.statusStrip1.Name = "statusStrip1";
            // splitMain
            this.splitMain.Dock = DockStyle.Fill;
            this.splitMain.Name = "splitMain";
            // tvFolders
            this.tvFolders.Location = new System.Drawing.Point(5, 5);
            this.tvFolders.Size = new System.Drawing.Size(200, 650);
            this.tvFolders.Name = "tvFolders";
            this.tvFolders.AfterSelect += new System.EventHandler(this.tvFolders_AfterSelect);
            // lvEmails
            this.lvEmails.Location = new System.Drawing.Point(210, 5);
            this.lvEmails.Size = new System.Drawing.Size(500, 350);
            this.lvEmails.Name = "lvEmails";
            this.lvEmails.SelectedIndexChanged += new System.EventHandler(this.lvEmails_SelectedIndexChanged);
            this.lvEmails.DoubleClick += new System.EventHandler(this.lvEmails_DoubleClick);
            // rtbBody
            this.rtbBody.Location = new System.Drawing.Point(210, 360);
            this.rtbBody.Size = new System.Drawing.Size(870, 300);
            this.rtbBody.Name = "rtbBody";
            // panelHeader
            this.panelHeader.Location = new System.Drawing.Point(210, 5);
            this.panelHeader.Size = new System.Drawing.Size(870, 80);
            this.panelHeader.Name = "panelHeader";
            // lblFrom
            this.lblFrom.Text = "From:";
            this.lblFrom.Location = new System.Drawing.Point(5, 5);
            this.lblFrom.Size = new System.Drawing.Size(50, 20);
            this.lblFrom.Name = "lblFrom";
            // lblFromValue
            this.lblFromValue.Text = "";
            this.lblFromValue.Location = new System.Drawing.Point(60, 5);
            this.lblFromValue.Size = new System.Drawing.Size(500, 20);
            this.lblFromValue.Name = "lblFromValue";
            // lblSubject
            this.lblSubject.Text = "Subject:";
            this.lblSubject.Location = new System.Drawing.Point(5, 30);
            this.lblSubject.Size = new System.Drawing.Size(50, 20);
            this.lblSubject.Name = "lblSubject";
            // lblSubjectValue
            this.lblSubjectValue.Text = "";
            this.lblSubjectValue.Location = new System.Drawing.Point(60, 30);
            this.lblSubjectValue.Size = new System.Drawing.Size(500, 20);
            this.lblSubjectValue.Name = "lblSubjectValue";
            // lblDate
            this.lblDate.Text = "Date:";
            this.lblDate.Location = new System.Drawing.Point(5, 55);
            this.lblDate.Size = new System.Drawing.Size(50, 20);
            this.lblDate.Name = "lblDate";
            // lblDateValue
            this.lblDateValue.Text = "";
            this.lblDateValue.Location = new System.Drawing.Point(60, 55);
            this.lblDateValue.Size = new System.Drawing.Size(500, 20);
            this.lblDateValue.Name = "lblDateValue";
            // btnCompose
            this.btnCompose.Text = "Compose";
            this.btnCompose.Location = new System.Drawing.Point(10, 660);
            this.btnCompose.Size = new System.Drawing.Size(90, 28);
            this.btnCompose.Name = "btnCompose";
            this.btnCompose.Click += new System.EventHandler(this.btnCompose_Click);
            // btnReply
            this.btnReply.Text = "Reply";
            this.btnReply.Location = new System.Drawing.Point(110, 660);
            this.btnReply.Size = new System.Drawing.Size(90, 28);
            this.btnReply.Name = "btnReply";
            this.btnReply.Click += new System.EventHandler(this.btnReply_Click);
            // btnForward
            this.btnForward.Text = "Forward";
            this.btnForward.Location = new System.Drawing.Point(210, 660);
            this.btnForward.Size = new System.Drawing.Size(90, 28);
            this.btnForward.Name = "btnForward";
            this.btnForward.Click += new System.EventHandler(this.btnForward_Click);
            // btnDelete
            this.btnDelete.Text = "Delete";
            this.btnDelete.Location = new System.Drawing.Point(310, 660);
            this.btnDelete.Size = new System.Drawing.Size(90, 28);
            this.btnDelete.Name = "btnDelete";
            this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);
            // btnRefresh
            this.btnRefresh.Text = "Refresh";
            this.btnRefresh.Location = new System.Drawing.Point(410, 660);
            this.btnRefresh.Size = new System.Drawing.Size(90, 28);
            this.btnRefresh.Name = "btnRefresh";
            this.btnRefresh.Click += new System.EventHandler(this.btnRefresh_Click);
            // txtSearch
            this.txtSearch.Location = new System.Drawing.Point(600, 660);
            this.txtSearch.Size = new System.Drawing.Size(200, 23);
            this.txtSearch.Name = "txtSearch";
            this.txtSearch.TextChanged += new System.EventHandler(this.txtSearch_TextChanged);
            // lblStatus
            this.lblStatus.Text = "Inbox (0 messages)";
            this.lblStatus.Location = new System.Drawing.Point(830, 665);
            this.lblStatus.Size = new System.Drawing.Size(250, 20);
            this.lblStatus.Name = "lblStatus";
            // checkMailTimer
            this.checkMailTimer.Name = "checkMailTimer";
            this.checkMailTimer.Tick += new System.EventHandler(this.checkMailTimer_Tick);
            // progressBar1
            this.progressBar1.Location = new System.Drawing.Point(830, 690);
            this.progressBar1.Size = new System.Drawing.Size(250, 15);
            this.progressBar1.Name = "progressBar1";
            // notifyIcon1
            this.notifyIcon1.Name = "notifyIcon1";
            // ctxMenu
            this.ctxMenu.Name = "ctxMenu";
            // EmailForm
            this.ClientSize = new System.Drawing.Size(1100, 750);
            this.Controls.Add(this.progressBar1);
            this.Controls.Add(this.lblStatus);
            this.Controls.Add(this.txtSearch);
            this.Controls.Add(this.btnRefresh);
            this.Controls.Add(this.btnDelete);
            this.Controls.Add(this.btnForward);
            this.Controls.Add(this.btnReply);
            this.Controls.Add(this.btnCompose);
            this.Controls.Add(this.lblDateValue);
            this.Controls.Add(this.lblDate);
            this.Controls.Add(this.lblSubjectValue);
            this.Controls.Add(this.lblSubject);
            this.Controls.Add(this.lblFromValue);
            this.Controls.Add(this.lblFrom);
            this.Controls.Add(this.panelHeader);
            this.Controls.Add(this.rtbBody);
            this.Controls.Add(this.lvEmails);
            this.Controls.Add(this.tvFolders);
            this.Controls.Add(this.splitMain);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.toolStrip1);
            this.Controls.Add(this.menuStrip1);
            this.Name = "EmailForm";
            this.Text = "Email Client";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.SplitContainer splitMain;
        private System.Windows.Forms.TreeView tvFolders;
        private System.Windows.Forms.ListView lvEmails;
        private System.Windows.Forms.RichTextBox rtbBody;
        private System.Windows.Forms.Panel panelHeader;
        private System.Windows.Forms.Label lblFrom;
        private System.Windows.Forms.Label lblFromValue;
        private System.Windows.Forms.Label lblSubject;
        private System.Windows.Forms.Label lblSubjectValue;
        private System.Windows.Forms.Label lblDate;
        private System.Windows.Forms.Label lblDateValue;
        private System.Windows.Forms.Button btnCompose;
        private System.Windows.Forms.Button btnReply;
        private System.Windows.Forms.Button btnForward;
        private System.Windows.Forms.Button btnDelete;
        private System.Windows.Forms.Button btnRefresh;
        private System.Windows.Forms.TextBox txtSearch;
        private System.Windows.Forms.Label lblStatus;
        private System.Windows.Forms.Timer checkMailTimer;
        private System.Windows.Forms.ProgressBar progressBar1;
        private System.Windows.Forms.NotifyIcon notifyIcon1;
        private System.Windows.Forms.ContextMenuStrip ctxMenu;
    }
}