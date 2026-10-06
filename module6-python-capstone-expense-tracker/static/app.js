const $ = (id) => document.getElementById(id);

const form = $("expenseForm");
const expenseId = $("expenseId");
const title = $("title");
const amount = $("amount");
const category = $("category");
const expenseDate = $("expenseDate");
const notes = $("notes");
const saveBtn = $("saveBtn");
const cancelBtn = $("cancelBtn");
const formMessage = $("formMessage");
const rows = $("expenseRows");
const emptyState = $("emptyState");
const search = $("search");
const filterCategory = $("filterCategory");

let allExpenses = [];

expenseDate.value = new Date().toISOString().slice(0, 10);

async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: {"Content-Type": "application/json", ...(options.headers || {})},
    ...options,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}

function money(value) {
  return `₹${Number(value).toLocaleString("en-IN", {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
}

function renderSummary(expenses) {
  const total = expenses.reduce((sum, item) => sum + Number(item.amount), 0);
  $("totalAmount").textContent = money(total);
  $("expenseCount").textContent = `${expenses.length} transaction${expenses.length === 1 ? "" : "s"}`;
}

function renderBars(expenses) {
  const totals = {};
  expenses.forEach(item => totals[item.category] = (totals[item.category] || 0) + Number(item.amount));
  const sorted = Object.entries(totals).sort((a,b) => b[1] - a[1]);
  const max = sorted[0]?.[1] || 1;
  $("categoryBars").innerHTML = sorted.length ? sorted.map(([name, total]) => `
    <div class="bar-row">
      <span>${escapeHtml(name)}</span>
      <div class="bar-track"><div class="bar-fill" style="width:${(total/max)*100}%"></div></div>
      <strong>${money(total)}</strong>
    </div>
  `).join("") : `<div class="empty">Add expenses to see your spending breakdown.</div>`;
}

function renderTable(expenses) {
  rows.innerHTML = expenses.map(item => `
    <tr>
      <td><strong>${escapeHtml(item.title)}</strong><br><small>${escapeHtml(item.notes || "")}</small></td>
      <td>${escapeHtml(item.category)}</td>
      <td>${escapeHtml(item.expense_date)}</td>
      <td class="amount">${money(item.amount)}</td>
      <td>
        <div class="actions">
          <button class="action" onclick="editExpense(${item.id})">Edit</button>
          <button class="action delete" onclick="deleteExpense(${item.id})">Delete</button>
        </div>
      </td>
    </tr>
  `).join("");
  emptyState.classList.toggle("hidden", expenses.length !== 0);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[ch]));
}

async function loadExpenses() {
  try {
    const params = new URLSearchParams();
    if (filterCategory.value) params.set("category", filterCategory.value);
    if (search.value.trim()) params.set("search", search.value.trim());

    allExpenses = await api(`/api/expenses?${params.toString()}`);
    renderSummary(allExpenses);
    renderBars(allExpenses);
    renderTable(allExpenses);
  } catch (error) {
    formMessage.textContent = error.message;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formMessage.textContent = "";

  const payload = {
    title: title.value,
    amount: amount.value,
    category: category.value,
    expense_date: expenseDate.value,
    notes: notes.value,
  };

  try {
    const id = expenseId.value;
    await api(id ? `/api/expenses/${id}` : "/api/expenses", {
      method: id ? "PUT" : "POST",
      body: JSON.stringify(payload),
    });
    resetForm();
    await loadExpenses();
  } catch (error) {
    formMessage.textContent = error.message;
  }
});

window.editExpense = function(id) {
  const item = allExpenses.find(expense => expense.id === id);
  if (!item) return;
  expenseId.value = item.id;
  title.value = item.title;
  amount.value = item.amount;
  category.value = item.category;
  expenseDate.value = item.expense_date;
  notes.value = item.notes || "";
  saveBtn.textContent = "Update expense";
  cancelBtn.classList.remove("hidden");
  window.scrollTo({top: 0, behavior: "smooth"});
};

window.deleteExpense = async function(id) {
  if (!confirm("Delete this expense?")) return;
  try {
    await api(`/api/expenses/${id}`, {method: "DELETE"});
    await loadExpenses();
  } catch (error) {
    formMessage.textContent = error.message;
  }
};

function resetForm() {
  form.reset();
  expenseId.value = "";
  expenseDate.value = new Date().toISOString().slice(0, 10);
  saveBtn.textContent = "Add expense";
  cancelBtn.classList.add("hidden");
  formMessage.textContent = "";
}

cancelBtn.addEventListener("click", resetForm);
filterCategory.addEventListener("change", loadExpenses);
let timer;
search.addEventListener("input", () => {
  clearTimeout(timer);
  timer = setTimeout(loadExpenses, 250);
});

loadExpenses();
