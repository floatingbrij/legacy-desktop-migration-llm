namespace ContactsManager
{
    partial class ContactsForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.lblName = new System.Windows.Forms.Label();
            this.txtName = new System.Windows.Forms.TextBox();
            this.lblEmail = new System.Windows.Forms.Label();
            this.txtEmail = new System.Windows.Forms.TextBox();
            this.lblPhone = new System.Windows.Forms.Label();
            this.txtPhone = new System.Windows.Forms.TextBox();
            this.btnAdd = new System.Windows.Forms.Button();
            this.btnDelete = new System.Windows.Forms.Button();
            this.btnEdit = new System.Windows.Forms.Button();
            this.lvContacts = new System.Windows.Forms.ListView();
            this.txtSearch = new System.Windows.Forms.TextBox();
            this.lblSearch = new System.Windows.Forms.Label();
            this.lblCount = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // lblName
            this.lblName.Text = "Name:";
            this.lblName.Location = new System.Drawing.Point(20, 20);
            this.lblName.Size = new System.Drawing.Size(60, 20);
            this.lblName.Name = "lblName";
            // txtName
            this.txtName.Location = new System.Drawing.Point(90, 17);
            this.txtName.Size = new System.Drawing.Size(200, 23);
            this.txtName.Name = "txtName";
            this.txtName.TextChanged += new System.EventHandler(this.txtName_TextChanged);
            // lblEmail
            this.lblEmail.Text = "Email:";
            this.lblEmail.Location = new System.Drawing.Point(20, 50);
            this.lblEmail.Size = new System.Drawing.Size(60, 20);
            this.lblEmail.Name = "lblEmail";
            // txtEmail
            this.txtEmail.Location = new System.Drawing.Point(90, 47);
            this.txtEmail.Size = new System.Drawing.Size(200, 23);
            this.txtEmail.Name = "txtEmail";
            // lblPhone
            this.lblPhone.Text = "Phone:";
            this.lblPhone.Location = new System.Drawing.Point(20, 80);
            this.lblPhone.Size = new System.Drawing.Size(60, 20);
            this.lblPhone.Name = "lblPhone";
            // txtPhone
            this.txtPhone.Location = new System.Drawing.Point(90, 77);
            this.txtPhone.Size = new System.Drawing.Size(200, 23);
            this.txtPhone.Name = "txtPhone";
            // btnAdd
            this.btnAdd.Text = "Add";
            this.btnAdd.Location = new System.Drawing.Point(310, 17);
            this.btnAdd.Size = new System.Drawing.Size(75, 28);
            this.btnAdd.Name = "btnAdd";
            this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);
            // btnDelete
            this.btnDelete.Text = "Delete";
            this.btnDelete.Location = new System.Drawing.Point(310, 50);
            this.btnDelete.Size = new System.Drawing.Size(75, 28);
            this.btnDelete.Name = "btnDelete";
            this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);
            // btnEdit
            this.btnEdit.Text = "Edit";
            this.btnEdit.Location = new System.Drawing.Point(310, 83);
            this.btnEdit.Size = new System.Drawing.Size(75, 28);
            this.btnEdit.Name = "btnEdit";
            this.btnEdit.Click += new System.EventHandler(this.btnEdit_Click);
            // lvContacts
            this.lvContacts.Location = new System.Drawing.Point(20, 120);
            this.lvContacts.Size = new System.Drawing.Size(660, 300);
            this.lvContacts.Name = "lvContacts";
            this.lvContacts.SelectedIndexChanged += new System.EventHandler(this.lvContacts_SelectedIndexChanged);
            // txtSearch
            this.txtSearch.Location = new System.Drawing.Point(20, 430);
            this.txtSearch.Size = new System.Drawing.Size(200, 23);
            this.txtSearch.Name = "txtSearch";
            this.txtSearch.TextChanged += new System.EventHandler(this.txtSearch_TextChanged);
            // lblSearch
            this.lblSearch.Text = "Search:";
            this.lblSearch.Location = new System.Drawing.Point(20, 410);
            this.lblSearch.Size = new System.Drawing.Size(60, 20);
            this.lblSearch.Name = "lblSearch";
            // lblCount
            this.lblCount.Text = "0 contacts";
            this.lblCount.Location = new System.Drawing.Point(580, 430);
            this.lblCount.Size = new System.Drawing.Size(100, 20);
            this.lblCount.Name = "lblCount";
            // ContactsForm
            this.ClientSize = new System.Drawing.Size(700, 500);
            this.Controls.Add(this.lblCount);
            this.Controls.Add(this.lblSearch);
            this.Controls.Add(this.txtSearch);
            this.Controls.Add(this.lvContacts);
            this.Controls.Add(this.btnEdit);
            this.Controls.Add(this.btnDelete);
            this.Controls.Add(this.btnAdd);
            this.Controls.Add(this.txtPhone);
            this.Controls.Add(this.lblPhone);
            this.Controls.Add(this.txtEmail);
            this.Controls.Add(this.lblEmail);
            this.Controls.Add(this.txtName);
            this.Controls.Add(this.lblName);
            this.Name = "ContactsForm";
            this.Text = "Contacts Manager";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Label lblName;
        private System.Windows.Forms.TextBox txtName;
        private System.Windows.Forms.Label lblEmail;
        private System.Windows.Forms.TextBox txtEmail;
        private System.Windows.Forms.Label lblPhone;
        private System.Windows.Forms.TextBox txtPhone;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.Button btnDelete;
        private System.Windows.Forms.Button btnEdit;
        private System.Windows.Forms.ListView lvContacts;
        private System.Windows.Forms.TextBox txtSearch;
        private System.Windows.Forms.Label lblSearch;
        private System.Windows.Forms.Label lblCount;
    }
}