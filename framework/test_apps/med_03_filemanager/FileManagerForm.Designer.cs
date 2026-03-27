namespace FileManagerApp
{
    partial class FileManagerForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.tvFolders = new System.Windows.Forms.TreeView();
            this.lvFiles = new System.Windows.Forms.ListView();
            this.txtPath = new System.Windows.Forms.TextBox();
            this.btnGo = new System.Windows.Forms.Button();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.toolStrip1 = new System.Windows.Forms.ToolStrip();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.panelToolbar = new System.Windows.Forms.Panel();
            this.ctxMenu = new System.Windows.Forms.ContextMenuStrip();
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.lblStatus = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // tvFolders
            this.tvFolders.Location = new System.Drawing.Point(10, 40);
            this.tvFolders.Size = new System.Drawing.Size(250, 460);
            this.tvFolders.Name = "tvFolders";
            this.tvFolders.AfterSelect += new System.EventHandler(this.tvFolders_AfterSelect);
            // lvFiles
            this.lvFiles.Location = new System.Drawing.Point(270, 40);
            this.lvFiles.Size = new System.Drawing.Size(510, 460);
            this.lvFiles.Name = "lvFiles";
            this.lvFiles.DoubleClick += new System.EventHandler(this.lvFiles_DoubleClick);
            // txtPath
            this.txtPath.Location = new System.Drawing.Point(10, 10);
            this.txtPath.Size = new System.Drawing.Size(700, 23);
            this.txtPath.Name = "txtPath";
            this.txtPath.KeyDown += new System.EventHandler(this.txtPath_KeyDown);
            // btnGo
            this.btnGo.Text = "Go";
            this.btnGo.Location = new System.Drawing.Point(720, 10);
            this.btnGo.Size = new System.Drawing.Size(60, 25);
            this.btnGo.Name = "btnGo";
            this.btnGo.Click += new System.EventHandler(this.btnGo_Click);
            // menuStrip1
            this.menuStrip1.Name = "menuStrip1";
            // toolStrip1
            this.toolStrip1.Name = "toolStrip1";
            // statusStrip1
            this.statusStrip1.Name = "statusStrip1";
            // splitContainer1
            this.splitContainer1.Location = new System.Drawing.Point(0, 60);
            this.splitContainer1.Size = new System.Drawing.Size(800, 470);
            this.splitContainer1.Name = "splitContainer1";
            // panelToolbar
            this.panelToolbar.Size = new System.Drawing.Size(800, 35);
            this.panelToolbar.Dock = DockStyle.Top;
            this.panelToolbar.Name = "panelToolbar";
            // ctxMenu
            this.ctxMenu.Name = "ctxMenu";
            // progressBar1
            this.progressBar1.Location = new System.Drawing.Point(10, 520);
            this.progressBar1.Size = new System.Drawing.Size(770, 15);
            this.progressBar1.Visible = false;
            this.progressBar1.Name = "progressBar1";
            // lblStatus
            this.lblStatus.Text = "Ready";
            this.lblStatus.Location = new System.Drawing.Point(10, 505);
            this.lblStatus.Size = new System.Drawing.Size(300, 20);
            this.lblStatus.Name = "lblStatus";
            // FileManagerForm
            this.ClientSize = new System.Drawing.Size(800, 550);
            this.Controls.Add(this.lblStatus);
            this.Controls.Add(this.progressBar1);
            this.Controls.Add(this.panelToolbar);
            this.Controls.Add(this.splitContainer1);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.toolStrip1);
            this.Controls.Add(this.menuStrip1);
            this.Controls.Add(this.btnGo);
            this.Controls.Add(this.txtPath);
            this.Controls.Add(this.lvFiles);
            this.Controls.Add(this.tvFolders);
            this.Name = "FileManagerForm";
            this.Text = "File Manager";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.TreeView tvFolders;
        private System.Windows.Forms.ListView lvFiles;
        private System.Windows.Forms.TextBox txtPath;
        private System.Windows.Forms.Button btnGo;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.SplitContainer splitContainer1;
        private System.Windows.Forms.Panel panelToolbar;
        private System.Windows.Forms.ContextMenuStrip ctxMenu;
        private System.Windows.Forms.ProgressBar progressBar1;
        private System.Windows.Forms.Label lblStatus;
    }
}