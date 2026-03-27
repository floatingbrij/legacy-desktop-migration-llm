"""
Test App Generator
===================
Generates synthetic WinForms .Designer.cs and .cs files
at different complexity levels for experiment evaluation.
"""
import os
import random

BASE = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(BASE, "test_apps")

# ---- Small apps (3-5 controls each, 1-2 events) ----

SMALL_APPS = {
    "small_03_about": {
        "namespace": "AboutApp",
        "class": "AboutForm",
        "title": "About",
        "size": (300, 200),
        "controls": [
            ("Label", "lblAppName", {"Text": "My Application", "Font": ("Segoe UI", 14), "Location": (50, 20), "Size": (200, 30)}),
            ("Label", "lblVersion", {"Text": "Version 1.0.0", "Location": (50, 60), "Size": (200, 20)}),
            ("Label", "lblCopyright", {"Text": "(c) 2024 Company", "Location": (50, 90), "Size": (200, 20)}),
            ("Button", "btnOK", {"Text": "OK", "Location": (100, 130), "Size": (90, 30), "events": [("Click", "btnOK_Click")]}),
            ("LinkLabel", "lnkWebsite", {"Text": "www.example.com", "Location": (50, 120), "Size": (200, 20)}),
        ],
        "handlers": {"btnOK_Click": "this.Close();"}
    },
    "small_04_settings": {
        "namespace": "SettingsApp",
        "class": "SettingsForm",
        "title": "Settings",
        "size": (350, 250),
        "controls": [
            ("Label", "lblTheme", {"Text": "Theme:", "Location": (20, 20), "Size": (80, 20)}),
            ("ComboBox", "cmbTheme", {"Location": (110, 17), "Size": (200, 23), "events": [("SelectedIndexChanged", "cmbTheme_SelectedIndexChanged")]}),
            ("CheckBox", "chkAutoSave", {"Text": "Auto-save", "Location": (20, 60), "Size": (150, 20), "events": [("CheckedChanged", "chkAutoSave_CheckedChanged")]}),
            ("CheckBox", "chkNotify", {"Text": "Notifications", "Location": (20, 90), "Size": (150, 20)}),
            ("Button", "btnSave", {"Text": "Save", "Location": (120, 180), "Size": (90, 30), "events": [("Click", "btnSave_Click")]}),
            ("Button", "btnCancel", {"Text": "Cancel", "Location": (220, 180), "Size": (90, 30), "events": [("Click", "btnCancel_Click")]}),
        ],
        "handlers": {
            "cmbTheme_SelectedIndexChanged": 'lblTheme.Text = "Theme: " + cmbTheme.SelectedItem.ToString();',
            "chkAutoSave_CheckedChanged": 'if (chkAutoSave.Checked) { /* enable */ }',
            "btnSave_Click": 'MessageBox.Show("Settings saved!"); this.Close();',
            "btnCancel_Click": "this.Close();"
        }
    },
    "small_05_timer": {
        "namespace": "TimerApp",
        "class": "TimerForm",
        "title": "Timer",
        "size": (280, 180),
        "controls": [
            ("Label", "lblTime", {"Text": "00:00:00", "Font": ("Segoe UI", 24), "Location": (40, 20), "Size": (200, 50)}),
            ("Button", "btnStart", {"Text": "Start", "Location": (20, 90), "Size": (75, 30), "events": [("Click", "btnStart_Click")]}),
            ("Button", "btnStop", {"Text": "Stop", "Location": (100, 90), "Size": (75, 30), "events": [("Click", "btnStop_Click")]}),
            ("Button", "btnReset", {"Text": "Reset", "Location": (180, 90), "Size": (75, 30), "events": [("Click", "btnReset_Click")]}),
            ("Timer", "timer1", {"events": [("Tick", "timer1_Tick")]}),
        ],
        "handlers": {
            "btnStart_Click": "timer1.Start();",
            "btnStop_Click": "timer1.Stop();",
            "btnReset_Click": 'timer1.Stop(); lblTime.Text = "00:00:00";',
            "timer1_Tick": 'TimeSpan ts = DateTime.Now - startTime;\nlblTime.Text = ts.ToString(@"hh\\:mm\\:ss");'
        }
    },
}

# ---- Medium apps (8-15 controls, 4-8 events) ----

MEDIUM_APPS = {
    "med_01_notepad": {
        "namespace": "SimpleNotepad",
        "class": "NotepadForm",
        "title": "Notepad",
        "size": (600, 450),
        "controls": [
            ("MenuStrip", "menuStrip1", {"Dock": "DockStyle.Top"}),
            ("ToolStrip", "toolStrip1", {}),
            ("RichTextBox", "rtbEditor", {"Dock": "DockStyle.Fill", "events": [("TextChanged", "rtbEditor_TextChanged")]}),
            ("StatusStrip", "statusStrip1", {"Dock": "DockStyle.Bottom"}),
            ("Button", "btnNew", {"Text": "New", "Location": (10, 50), "Size": (60, 25), "events": [("Click", "btnNew_Click")]}),
            ("Button", "btnOpen", {"Text": "Open", "Location": (75, 50), "Size": (60, 25), "events": [("Click", "btnOpen_Click")]}),
            ("Button", "btnSave", {"Text": "Save", "Location": (140, 50), "Size": (60, 25), "events": [("Click", "btnSave_Click")]}),
            ("Label", "lblStatus", {"Text": "Ready", "Location": (10, 420), "Size": (200, 20)}),
            ("ComboBox", "cmbFontSize", {"Location": (220, 50), "Size": (80, 25), "events": [("SelectedIndexChanged", "cmbFontSize_Changed")]}),
            ("CheckBox", "chkWordWrap", {"Text": "Word Wrap", "Location": (310, 52), "Size": (100, 20), "events": [("CheckedChanged", "chkWordWrap_Changed")]}),
        ],
        "handlers": {
            "rtbEditor_TextChanged": 'lblStatus.Text = $"Characters: {rtbEditor.Text.Length}";',
            "btnNew_Click": 'if (MessageBox.Show("New document?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)\n    rtbEditor.Text = "";',
            "btnOpen_Click": 'OpenFileDialog ofd = new OpenFileDialog();\nofd.Filter = "Text files|*.txt";\nif (ofd.ShowDialog() == DialogResult.OK)\n    rtbEditor.Text = System.IO.File.ReadAllText(ofd.FileName);',
            "btnSave_Click": 'SaveFileDialog sfd = new SaveFileDialog();\nsfd.Filter = "Text files|*.txt";\nif (sfd.ShowDialog() == DialogResult.OK)\n    System.IO.File.WriteAllText(sfd.FileName, rtbEditor.Text);',
            "cmbFontSize_Changed": 'float size = float.Parse(cmbFontSize.SelectedItem.ToString());\nrtbEditor.Font = new System.Drawing.Font(rtbEditor.Font.FontFamily, size);',
            "chkWordWrap_Changed": "rtbEditor.WordWrap = chkWordWrap.Checked;"
        }
    },
    "med_02_contacts": {
        "namespace": "ContactsManager",
        "class": "ContactsForm",
        "title": "Contacts Manager",
        "size": (700, 500),
        "controls": [
            ("Label", "lblName", {"Text": "Name:", "Location": (20, 20), "Size": (60, 20)}),
            ("TextBox", "txtName", {"Location": (90, 17), "Size": (200, 23), "events": [("TextChanged", "txtName_TextChanged")]}),
            ("Label", "lblEmail", {"Text": "Email:", "Location": (20, 50), "Size": (60, 20)}),
            ("TextBox", "txtEmail", {"Location": (90, 47), "Size": (200, 23)}),
            ("Label", "lblPhone", {"Text": "Phone:", "Location": (20, 80), "Size": (60, 20)}),
            ("TextBox", "txtPhone", {"Location": (90, 77), "Size": (200, 23)}),
            ("Button", "btnAdd", {"Text": "Add", "Location": (310, 17), "Size": (75, 28), "events": [("Click", "btnAdd_Click")]}),
            ("Button", "btnDelete", {"Text": "Delete", "Location": (310, 50), "Size": (75, 28), "events": [("Click", "btnDelete_Click")]}),
            ("Button", "btnEdit", {"Text": "Edit", "Location": (310, 83), "Size": (75, 28), "events": [("Click", "btnEdit_Click")]}),
            ("ListView", "lvContacts", {"Location": (20, 120), "Size": (660, 300), "events": [("SelectedIndexChanged", "lvContacts_SelectedIndexChanged")]}),
            ("TextBox", "txtSearch", {"Location": (20, 430), "Size": (200, 23), "events": [("TextChanged", "txtSearch_TextChanged")]}),
            ("Label", "lblSearch", {"Text": "Search:", "Location": (20, 410), "Size": (60, 20)}),
            ("Label", "lblCount", {"Text": "0 contacts", "Location": (580, 430), "Size": (100, 20)}),
        ],
        "handlers": {
            "txtName_TextChanged": 'btnAdd.Enabled = txtName.Text.Length > 0;',
            "btnAdd_Click": 'ListViewItem item = new ListViewItem(txtName.Text);\nitem.SubItems.Add(txtEmail.Text);\nitem.SubItems.Add(txtPhone.Text);\nlvContacts.Items.Add(item);\nlblCount.Text = $"{lvContacts.Items.Count} contacts";',
            "btnDelete_Click": 'if (lvContacts.SelectedItems.Count > 0)\n{\n    lvContacts.Items.Remove(lvContacts.SelectedItems[0]);\n    lblCount.Text = $"{lvContacts.Items.Count} contacts";\n}',
            "btnEdit_Click": 'if (lvContacts.SelectedItems.Count > 0)\n{\n    lvContacts.SelectedItems[0].Text = txtName.Text;\n    lvContacts.SelectedItems[0].SubItems[1].Text = txtEmail.Text;\n}',
            "lvContacts_SelectedIndexChanged": 'if (lvContacts.SelectedItems.Count > 0)\n{\n    txtName.Text = lvContacts.SelectedItems[0].Text;\n    txtEmail.Text = lvContacts.SelectedItems[0].SubItems[1].Text;\n}',
            "txtSearch_TextChanged": 'foreach (ListViewItem item in lvContacts.Items)\n{\n    item.BackColor = item.Text.Contains(txtSearch.Text) ? System.Drawing.Color.Yellow : System.Drawing.Color.White;\n}'
        }
    },
    "med_03_filemanager": {
        "namespace": "FileManagerApp",
        "class": "FileManagerForm",
        "title": "File Manager",
        "size": (800, 550),
        "controls": [
            ("TreeView", "tvFolders", {"Location": (10, 40), "Size": (250, 460), "events": [("AfterSelect", "tvFolders_AfterSelect")]}),
            ("ListView", "lvFiles", {"Location": (270, 40), "Size": (510, 460), "events": [("DoubleClick", "lvFiles_DoubleClick")]}),
            ("TextBox", "txtPath", {"Location": (10, 10), "Size": (700, 23), "events": [("KeyDown", "txtPath_KeyDown")]}),
            ("Button", "btnGo", {"Text": "Go", "Location": (720, 10), "Size": (60, 25), "events": [("Click", "btnGo_Click")]}),
            ("MenuStrip", "menuStrip1", {}),
            ("ToolStrip", "toolStrip1", {}),
            ("StatusStrip", "statusStrip1", {}),
            ("SplitContainer", "splitContainer1", {"Location": (0, 60), "Size": (800, 470)}),
            ("Panel", "panelToolbar", {"Dock": "DockStyle.Top", "Size": (800, 35)}),
            ("ContextMenuStrip", "ctxMenu", {}),
            ("ProgressBar", "progressBar1", {"Location": (10, 520), "Size": (770, 15), "Visible": "false"}),
            ("Label", "lblStatus", {"Text": "Ready", "Location": (10, 505), "Size": (300, 20)}),
        ],
        "handlers": {
            "tvFolders_AfterSelect": 'string path = tvFolders.SelectedNode.Tag.ToString();\ntxtPath.Text = path;\nLoadFiles(path);',
            "lvFiles_DoubleClick": 'if (lvFiles.SelectedItems.Count > 0)\n{\n    string file = lvFiles.SelectedItems[0].Tag.ToString();\n    System.Diagnostics.Process.Start(file);\n}',
            "txtPath_KeyDown": 'if (e.KeyCode == Keys.Enter)\n    LoadPath(txtPath.Text);',
            "btnGo_Click": 'LoadPath(txtPath.Text);'
        }
    },
    "med_04_imageviewer": {
        "namespace": "ImageViewerApp",
        "class": "ImageViewerForm",
        "title": "Image Viewer",
        "size": (800, 600),
        "controls": [
            ("PictureBox", "picMain", {"Dock": "DockStyle.Fill", "SizeMode": "Zoom"}),
            ("MenuStrip", "menuStrip1", {}),
            ("ToolStrip", "toolStrip1", {}),
            ("StatusStrip", "statusStrip1", {}),
            ("Panel", "panelBottom", {"Dock": "DockStyle.Bottom", "Size": (800, 50)}),
            ("Button", "btnPrev", {"Text": "<", "Location": (300, 10), "Size": (40, 30), "events": [("Click", "btnPrev_Click")]}),
            ("Button", "btnNext", {"Text": ">", "Location": (460, 10), "Size": (40, 30), "events": [("Click", "btnNext_Click")]}),
            ("TrackBar", "trackZoom", {"Location": (520, 10), "Size": (200, 30), "events": [("Scroll", "trackZoom_Scroll")]}),
            ("Label", "lblFileName", {"Text": "", "Location": (10, 15), "Size": (280, 20)}),
            ("Label", "lblZoom", {"Text": "100%", "Location": (730, 15), "Size": (50, 20)}),
            ("ProgressBar", "progressLoad", {"Location": (350, 15), "Size": (100, 20), "Visible": "false"}),
        ],
        "handlers": {
            "btnPrev_Click": 'if (currentIndex > 0) { currentIndex--; LoadImage(files[currentIndex]); }',
            "btnNext_Click": 'if (currentIndex < files.Length - 1) { currentIndex++; LoadImage(files[currentIndex]); }',
            "trackZoom_Scroll": 'float zoom = trackZoom.Value / 100f;\npicMain.Width = (int)(originalWidth * zoom);\npicMain.Height = (int)(originalHeight * zoom);\nlblZoom.Text = $"{trackZoom.Value}%";'
        }
    },
}

# ---- Large apps (16+ controls, 8+ events) ----

LARGE_APPS = {
    "large_01_inventory": {
        "namespace": "InventorySystem",
        "class": "InventoryForm",
        "title": "Inventory Manager",
        "size": (1024, 700),
        "controls": [
            ("MenuStrip", "menuStrip1", {}),
            ("ToolStrip", "toolStrip1", {}),
            ("StatusStrip", "statusStrip1", {}),
            ("TabControl", "tabMain", {"Location": (10, 60), "Size": (1000, 580)}),
            ("DataGridView", "dgvProducts", {"Location": (10, 30), "Size": (970, 350), "events": [("CellClick", "dgvProducts_CellClick"), ("CellValueChanged", "dgvProducts_CellValueChanged")]}),
            ("Panel", "panelDetails", {"Location": (10, 400), "Size": (970, 170)}),
            ("Label", "lblProductName", {"Text": "Product:", "Location": (20, 10), "Size": (70, 20)}),
            ("TextBox", "txtProductName", {"Location": (100, 7), "Size": (250, 23), "events": [("TextChanged", "txtProductName_TextChanged")]}),
            ("Label", "lblCategory", {"Text": "Category:", "Location": (20, 40), "Size": (70, 20)}),
            ("ComboBox", "cmbCategory", {"Location": (100, 37), "Size": (250, 23), "events": [("SelectedIndexChanged", "cmbCategory_Changed")]}),
            ("Label", "lblPrice", {"Text": "Price:", "Location": (370, 10), "Size": (50, 20)}),
            ("NumericUpDown", "nudPrice", {"Location": (430, 7), "Size": (120, 23), "events": [("ValueChanged", "nudPrice_ValueChanged")]}),
            ("Label", "lblQuantity", {"Text": "Quantity:", "Location": (370, 40), "Size": (50, 20)}),
            ("NumericUpDown", "nudQuantity", {"Location": (430, 37), "Size": (120, 23)}),
            ("Button", "btnAdd", {"Text": "Add Product", "Location": (580, 7), "Size": (110, 28), "events": [("Click", "btnAdd_Click")]}),
            ("Button", "btnUpdate", {"Text": "Update", "Location": (580, 40), "Size": (110, 28), "events": [("Click", "btnUpdate_Click")]}),
            ("Button", "btnDelete", {"Text": "Delete", "Location": (700, 7), "Size": (90, 28), "events": [("Click", "btnDelete_Click")]}),
            ("Button", "btnExport", {"Text": "Export CSV", "Location": (700, 40), "Size": (90, 28), "events": [("Click", "btnExport_Click")]}),
            ("TextBox", "txtSearch", {"Location": (800, 7), "Size": (170, 23), "events": [("TextChanged", "txtSearch_TextChanged")]}),
            ("Label", "lblSearch", {"Text": "Search:", "Location": (800, 40), "Size": (170, 20)}),
            ("CheckBox", "chkLowStock", {"Text": "Low Stock Only", "Location": (800, 60), "Size": (120, 20), "events": [("CheckedChanged", "chkLowStock_Changed")]}),
            ("Label", "lblTotal", {"Text": "Total: 0 items", "Location": (10, 660), "Size": (200, 20)}),
            ("Label", "lblValue", {"Text": "Total Value: $0.00", "Location": (300, 660), "Size": (200, 20)}),
            ("ProgressBar", "progressBar1", {"Location": (650, 660), "Size": (350, 15)}),
            ("Timer", "autoRefreshTimer", {"events": [("Tick", "autoRefreshTimer_Tick")]}),
            ("DateTimePicker", "dtpDate", {"Location": (580, 70), "Size": (200, 23)}),
        ],
        "handlers": {
            "dgvProducts_CellClick": 'if (dgvProducts.CurrentRow != null)\n{\n    txtProductName.Text = dgvProducts.CurrentRow.Cells[0].Value.ToString();\n    cmbCategory.Text = dgvProducts.CurrentRow.Cells[1].Value.ToString();\n    nudPrice.Value = Convert.ToDecimal(dgvProducts.CurrentRow.Cells[2].Value);\n    nudQuantity.Value = Convert.ToInt32(dgvProducts.CurrentRow.Cells[3].Value);\n}',
            "dgvProducts_CellValueChanged": 'UpdateTotals();',
            "txtProductName_TextChanged": 'btnAdd.Enabled = txtProductName.Text.Length > 0;',
            "cmbCategory_Changed": 'FilterByCategory(cmbCategory.SelectedItem?.ToString());',
            "nudPrice_ValueChanged": 'UpdateTotals();',
            "btnAdd_Click": 'dgvProducts.Rows.Add(txtProductName.Text, cmbCategory.Text, nudPrice.Value, nudQuantity.Value, DateTime.Now);\nUpdateTotals();\nClearFields();',
            "btnUpdate_Click": 'if (dgvProducts.CurrentRow != null)\n{\n    dgvProducts.CurrentRow.Cells[0].Value = txtProductName.Text;\n    dgvProducts.CurrentRow.Cells[1].Value = cmbCategory.Text;\n    dgvProducts.CurrentRow.Cells[2].Value = nudPrice.Value;\n    UpdateTotals();\n}',
            "btnDelete_Click": 'if (dgvProducts.CurrentRow != null && MessageBox.Show("Delete?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)\n{\n    dgvProducts.Rows.Remove(dgvProducts.CurrentRow);\n    UpdateTotals();\n}',
            "btnExport_Click": 'SaveFileDialog sfd = new SaveFileDialog();\nsfd.Filter = "CSV|*.csv";\nif (sfd.ShowDialog() == DialogResult.OK)\n{\n    using (var writer = new System.IO.StreamWriter(sfd.FileName))\n    {\n        foreach (DataGridViewRow row in dgvProducts.Rows)\n            writer.WriteLine(string.Join(",", row.Cells.Cast<DataGridViewCell>().Select(c => c.Value)));\n    }\n}',
            "txtSearch_TextChanged": 'foreach (DataGridViewRow row in dgvProducts.Rows)\n{\n    row.Visible = row.Cells[0].Value?.ToString().Contains(txtSearch.Text, StringComparison.OrdinalIgnoreCase) ?? false;\n}',
            "chkLowStock_Changed": 'foreach (DataGridViewRow row in dgvProducts.Rows)\n{\n    if (chkLowStock.Checked)\n        row.Visible = Convert.ToInt32(row.Cells[3].Value) < 10;\n    else\n        row.Visible = true;\n}',
            "autoRefreshTimer_Tick": 'UpdateTotals();\nlblTotal.Text = $"Total: {dgvProducts.Rows.Count} items";'
        }
    },
    "large_02_emailclient": {
        "namespace": "EmailClient",
        "class": "EmailForm",
        "title": "Email Client",
        "size": (1100, 750),
        "controls": [
            ("MenuStrip", "menuStrip1", {}),
            ("ToolStrip", "toolStrip1", {}),
            ("StatusStrip", "statusStrip1", {}),
            ("SplitContainer", "splitMain", {"Dock": "DockStyle.Fill"}),
            ("TreeView", "tvFolders", {"Location": (5, 5), "Size": (200, 650), "events": [("AfterSelect", "tvFolders_AfterSelect")]}),
            ("ListView", "lvEmails", {"Location": (210, 5), "Size": (500, 350), "events": [("SelectedIndexChanged", "lvEmails_SelectedIndexChanged"), ("DoubleClick", "lvEmails_DoubleClick")]}),
            ("RichTextBox", "rtbBody", {"Location": (210, 360), "Size": (870, 300)}),
            ("Panel", "panelHeader", {"Location": (210, 5), "Size": (870, 80)}),
            ("Label", "lblFrom", {"Text": "From:", "Location": (5, 5), "Size": (50, 20)}),
            ("Label", "lblFromValue", {"Text": "", "Location": (60, 5), "Size": (500, 20)}),
            ("Label", "lblSubject", {"Text": "Subject:", "Location": (5, 30), "Size": (50, 20)}),
            ("Label", "lblSubjectValue", {"Text": "", "Location": (60, 30), "Size": (500, 20)}),
            ("Label", "lblDate", {"Text": "Date:", "Location": (5, 55), "Size": (50, 20)}),
            ("Label", "lblDateValue", {"Text": "", "Location": (60, 55), "Size": (500, 20)}),
            ("Button", "btnCompose", {"Text": "Compose", "Location": (10, 660), "Size": (90, 28), "events": [("Click", "btnCompose_Click")]}),
            ("Button", "btnReply", {"Text": "Reply", "Location": (110, 660), "Size": (90, 28), "events": [("Click", "btnReply_Click")]}),
            ("Button", "btnForward", {"Text": "Forward", "Location": (210, 660), "Size": (90, 28), "events": [("Click", "btnForward_Click")]}),
            ("Button", "btnDelete", {"Text": "Delete", "Location": (310, 660), "Size": (90, 28), "events": [("Click", "btnDelete_Click")]}),
            ("Button", "btnRefresh", {"Text": "Refresh", "Location": (410, 660), "Size": (90, 28), "events": [("Click", "btnRefresh_Click")]}),
            ("TextBox", "txtSearch", {"Location": (600, 660), "Size": (200, 23), "events": [("TextChanged", "txtSearch_TextChanged")]}),
            ("Label", "lblStatus", {"Text": "Inbox (0 messages)", "Location": (830, 665), "Size": (250, 20)}),
            ("Timer", "checkMailTimer", {"events": [("Tick", "checkMailTimer_Tick")]}),
            ("ProgressBar", "progressBar1", {"Location": (830, 690), "Size": (250, 15)}),
            ("NotifyIcon", "notifyIcon1", {}),
            ("ContextMenuStrip", "ctxMenu", {}),
        ],
        "handlers": {
            "tvFolders_AfterSelect": 'LoadFolder(tvFolders.SelectedNode.Text);',
            "lvEmails_SelectedIndexChanged": 'if (lvEmails.SelectedItems.Count > 0)\n{\n    var email = (Email)lvEmails.SelectedItems[0].Tag;\n    lblFromValue.Text = email.From;\n    lblSubjectValue.Text = email.Subject;\n    lblDateValue.Text = email.Date.ToString();\n    rtbBody.Text = email.Body;\n}',
            "lvEmails_DoubleClick": 'if (lvEmails.SelectedItems.Count > 0)\n{\n    var compose = new ComposeForm((Email)lvEmails.SelectedItems[0].Tag);\n    compose.ShowDialog();\n}',
            "btnCompose_Click": 'var compose = new ComposeForm();\ncompose.ShowDialog();',
            "btnReply_Click": 'if (lvEmails.SelectedItems.Count > 0)\n    new ComposeForm((Email)lvEmails.SelectedItems[0].Tag, ComposeMode.Reply).ShowDialog();',
            "btnForward_Click": 'new ComposeForm(null, ComposeMode.Forward).ShowDialog();',
            "btnDelete_Click": 'if (lvEmails.SelectedItems.Count > 0 && MessageBox.Show("Delete email?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)\n{\n    lvEmails.Items.Remove(lvEmails.SelectedItems[0]);\n    lblStatus.Text = $"Inbox ({lvEmails.Items.Count} messages)";\n}',
            "btnRefresh_Click": 'progressBar1.Visible = true;\nBackgroundWorker bw = new BackgroundWorker();\nbw.DoWork += (s, ev) => { Thread.Sleep(2000); };\nbw.RunWorkerCompleted += (s, ev) => { this.Invoke((Action)(() => { LoadFolder("Inbox"); progressBar1.Visible = false; })); };\nbw.RunWorkerAsync();',
            "txtSearch_TextChanged": 'foreach (ListViewItem item in lvEmails.Items)\n    item.BackColor = item.Text.Contains(txtSearch.Text) ? System.Drawing.Color.Yellow : System.Drawing.Color.White;',
            "checkMailTimer_Tick": 'CheckNewMail();\nlblStatus.Text = $"Last check: {DateTime.Now:HH:mm:ss}";'
        }
    },
    "large_03_dashboard": {
        "namespace": "DashboardApp",
        "class": "DashboardForm",
        "title": "Dashboard",
        "size": (1200, 800),
        "controls": [
            ("MenuStrip", "menuStrip1", {}),
            ("Panel", "panelTop", {"Dock": "DockStyle.Top", "Size": (1200, 80)}),
            ("Panel", "panelLeft", {"Dock": "DockStyle.Left", "Size": (250, 720)}),
            ("Panel", "panelMain", {"Dock": "DockStyle.Fill"}),
            ("Label", "lblWelcome", {"Text": "Welcome, User", "Font": ("Segoe UI", 18), "Location": (20, 20), "Size": (300, 40)}),
            ("Label", "lblDate", {"Text": "March 28, 2026", "Location": (20, 55), "Size": (200, 20)}),
            ("Button", "btnDashboard", {"Text": "Dashboard", "Location": (10, 10), "Size": (230, 35), "events": [("Click", "btnDashboard_Click")]}),
            ("Button", "btnReports", {"Text": "Reports", "Location": (10, 50), "Size": (230, 35), "events": [("Click", "btnReports_Click")]}),
            ("Button", "btnUsers", {"Text": "Users", "Location": (10, 90), "Size": (230, 35), "events": [("Click", "btnUsers_Click")]}),
            ("Button", "btnSettings", {"Text": "Settings", "Location": (10, 130), "Size": (230, 35), "events": [("Click", "btnSettings_Click")]}),
            ("Button", "btnLogout", {"Text": "Logout", "Location": (10, 650), "Size": (230, 35), "events": [("Click", "btnLogout_Click")]}),
            ("DataGridView", "dgvData", {"Location": (10, 10), "Size": (700, 400), "events": [("CellClick", "dgvData_CellClick")]}),
            ("PictureBox", "picChart", {"Location": (10, 420), "Size": (700, 250)}),
            ("Panel", "panelStats", {"Location": (720, 10), "Size": (220, 660)}),
            ("Label", "lblStat1", {"Text": "Total Users: 0", "Location": (10, 10), "Size": (200, 25)}),
            ("Label", "lblStat2", {"Text": "Revenue: $0", "Location": (10, 40), "Size": (200, 25)}),
            ("Label", "lblStat3", {"Text": "Orders: 0", "Location": (10, 70), "Size": (200, 25)}),
            ("Label", "lblStat4", {"Text": "Pending: 0", "Location": (10, 100), "Size": (200, 25)}),
            ("DateTimePicker", "dtpStart", {"Location": (10, 140), "Size": (200, 23), "events": [("ValueChanged", "dtpStart_Changed")]}),
            ("DateTimePicker", "dtpEnd", {"Location": (10, 170), "Size": (200, 23), "events": [("ValueChanged", "dtpEnd_Changed")]}),
            ("Button", "btnRefresh", {"Text": "Refresh", "Location": (10, 200), "Size": (200, 30), "events": [("Click", "btnRefresh_Click")]}),
            ("ProgressBar", "progressBar1", {"Location": (10, 640), "Size": (200, 20)}),
            ("Timer", "refreshTimer", {"events": [("Tick", "refreshTimer_Tick")]}),
            ("ComboBox", "cmbView", {"Location": (10, 240), "Size": (200, 23), "events": [("SelectedIndexChanged", "cmbView_Changed")]}),
            ("CheckBox", "chkAutoRefresh", {"Text": "Auto-refresh", "Location": (10, 270), "Size": (200, 20), "events": [("CheckedChanged", "chkAutoRefresh_Changed")]}),
        ],
        "handlers": {
            "btnDashboard_Click": 'LoadDashboard();',
            "btnReports_Click": 'LoadReports();',
            "btnUsers_Click": 'LoadUsers();',
            "btnSettings_Click": 'var settings = new SettingsForm();\nsettings.ShowDialog();',
            "btnLogout_Click": 'if (MessageBox.Show("Logout?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)\n{\n    this.Hide();\n    new LoginForm().ShowDialog();\n    this.Close();\n}',
            "dgvData_CellClick": 'UpdateStats();',
            "dtpStart_Changed": 'FilterByDate();',
            "dtpEnd_Changed": 'FilterByDate();',
            "btnRefresh_Click": 'progressBar1.Value = 0;\nBackgroundWorker bw = new BackgroundWorker();\nbw.DoWork += (s, ev) => { for (int i = 0; i <= 100; i += 10) { Thread.Sleep(100); this.Invoke((Action)(() => progressBar1.Value = i)); } };\nbw.RunWorkerCompleted += (s, ev) => { LoadDashboard(); };\nbw.RunWorkerAsync();',
            "refreshTimer_Tick": 'LoadDashboard();',
            "cmbView_Changed": 'ChangeView(cmbView.SelectedItem.ToString());',
            "chkAutoRefresh_Changed": 'refreshTimer.Enabled = chkAutoRefresh.Checked;'
        }
    },
}


def gen_designer_cs(app_def: dict, folder: str):
    """Generate a .Designer.cs file from app definition."""
    ns = app_def["namespace"]
    cls = app_def["class"]
    title = app_def["title"]
    w, h = app_def["size"]

    lines = [f"namespace {ns}", "{", f"    partial class {cls}", "    {",
             "        private System.ComponentModel.IContainer components = null;",
             "        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }",
             "", "        private void InitializeComponent()", "        {"]

    # Declarations
    for ctrl_type, name, props in app_def["controls"]:
        full_type = f"System.Windows.Forms.{ctrl_type}"
        lines.append(f"            this.{name} = new {full_type}();")

    lines.append("            this.SuspendLayout();")

    # Properties
    for ctrl_type, name, props in app_def["controls"]:
        lines.append(f"            // {name}")
        if "Text" in props:
            lines.append(f'            this.{name}.Text = "{props["Text"]}";')
        if "Location" in props:
            x, y = props["Location"]
            lines.append(f"            this.{name}.Location = new System.Drawing.Point({x}, {y});")
        if "Size" in props:
            w2, h2 = props["Size"]
            lines.append(f"            this.{name}.Size = new System.Drawing.Size({w2}, {h2});")
        if "Font" in props:
            fn, fs = props["Font"]
            lines.append(f'            this.{name}.Font = new System.Drawing.Font("{fn}", {fs}F);')
        if "Dock" in props:
            lines.append(f"            this.{name}.Dock = {props['Dock']};")
        if "SizeMode" in props:
            lines.append(f"            this.{name}.SizeMode = System.Windows.Forms.PictureBoxSizeMode.{props['SizeMode']};")
        if "Visible" in props:
            lines.append(f"            this.{name}.Visible = {props['Visible']};")
        if "Enabled" in props:
            lines.append(f"            this.{name}.Enabled = {props['Enabled']};")
        if "ReadOnly" in props:
            lines.append(f"            this.{name}.ReadOnly = {props['ReadOnly']};")
        if "PasswordChar" in props:
            lines.append(f"            this.{name}.PasswordChar = '{props['PasswordChar']}';")
        lines.append(f'            this.{name}.Name = "{name}";')

        # Events
        for evt_name, handler in props.get("events", []):
            lines.append(f"            this.{name}.{evt_name} += new System.EventHandler(this.{handler});")

    # Form setup
    lines.append(f"            // {cls}")
    lines.append(f"            this.ClientSize = new System.Drawing.Size({w}, {h});")
    for ctrl_type, name, props in reversed(app_def["controls"]):
        if ctrl_type not in ("Timer", "ToolTip", "NotifyIcon", "ContextMenuStrip", "ImageList"):
            lines.append(f"            this.Controls.Add(this.{name});")
    lines.append(f'            this.Name = "{cls}";')
    lines.append(f'            this.Text = "{title}";')
    lines.append("            this.ResumeLayout(false);")
    lines.append("            this.PerformLayout();")
    lines.append("        }")
    lines.append("")

    # Field declarations
    for ctrl_type, name, props in app_def["controls"]:
        lines.append(f"        private System.Windows.Forms.{ctrl_type} {name};")

    lines.append("    }")
    lines.append("}")

    os.makedirs(folder, exist_ok=True)
    designer_path = os.path.join(folder, f"{cls}.Designer.cs")
    with open(designer_path, 'w') as f:
        f.write("\n".join(lines))

    return designer_path


def gen_code_behind(app_def: dict, folder: str):
    """Generate a .cs code-behind file from app definition."""
    ns = app_def["namespace"]
    cls = app_def["class"]
    handlers = app_def.get("handlers", {})

    lines = [
        "using System;",
        "using System.Windows.Forms;",
        "using System.Drawing;",
        "",
        f"namespace {ns}",
        "{",
        f"    public partial class {cls} : Form",
        "    {",
        f"        public {cls}()",
        "        {",
        "            InitializeComponent();",
        "        }",
    ]

    for handler_name, body in handlers.items():
        lines.append("")
        lines.append(f"        private void {handler_name}(object sender, EventArgs e)")
        lines.append("        {")
        for body_line in body.split('\n'):
            lines.append(f"            {body_line}")
        lines.append("        }")

    lines.append("    }")
    lines.append("}")

    cs_path = os.path.join(folder, f"{cls}.cs")
    with open(cs_path, 'w') as f:
        f.write("\n".join(lines))

    return cs_path


def generate_all():
    """Generate all test apps."""
    all_apps = {}
    all_apps.update(SMALL_APPS)
    all_apps.update(MEDIUM_APPS)
    all_apps.update(LARGE_APPS)

    for app_name, app_def in all_apps.items():
        folder = os.path.join(TEST_DIR, app_name)
        gen_designer_cs(app_def, folder)
        gen_code_behind(app_def, folder)
        cls = app_def["class"]
        n_controls = len(app_def["controls"])
        n_handlers = len(app_def.get("handlers", {}))
        print(f"  Generated {app_name}: {cls} ({n_controls} controls, {n_handlers} handlers)")


if __name__ == "__main__":
    print("Generating test WinForms applications...")
    generate_all()
    print("Done!")
