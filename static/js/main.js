/**
 * ECOTECH SERVICES - Main JavaScript File
 * Handles interactive features and UI enhancements
 */

// Import Bootstrap
const bootstrap = window.bootstrap

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  initializeTooltips()

  // Initialize form validation
  initializeFormValidation()

  // Initialize file upload handling
  initializeFileUpload()

  // Initialize smooth scrolling
  initializeSmoothScrolling()

  // Initialize loading states
  initializeLoadingStates()

  // Initialize auto-dismiss alerts
  initializeAlerts()

  // Initialize search functionality
  initializeSearch()

  // Initialize table sorting
  initializeTableSorting()

  // Initialize copy to clipboard functionality
  initializeClipboard()
})

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))
}

/**
 * Initialize form validation and enhancement
 */
function initializeFormValidation() {
  const forms = document.querySelectorAll(".needs-validation")

  Array.prototype.slice.call(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add("was-validated")
      },
      false,
    )
  })

  // Real-time validation for email fields
  const emailInputs = document.querySelectorAll('input[type="email"]')
  emailInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      validateEmail(this)
    })
  })

  // Real-time validation for required fields
  const requiredInputs = document.querySelectorAll("input[required], textarea[required], select[required]")
  requiredInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      validateRequired(this)
    })
  })
}

/**
 * Validate email format
 */
function validateEmail(input) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  const isValid = emailRegex.test(input.value)

  if (input.value && !isValid) {
    input.classList.add("is-invalid")
    input.classList.remove("is-valid")
  } else if (input.value && isValid) {
    input.classList.add("is-valid")
    input.classList.remove("is-invalid")
  } else {
    input.classList.remove("is-valid", "is-invalid")
  }
}

/**
 * Validate required fields
 */
function validateRequired(input) {
  if (input.hasAttribute("required")) {
    if (!input.value.trim()) {
      input.classList.add("is-invalid")
      input.classList.remove("is-valid")
    } else {
      input.classList.add("is-valid")
      input.classList.remove("is-invalid")
    }
  }
}

/**
 * Initialize file upload handling
 */
function initializeFileUpload() {
  const fileInputs = document.querySelectorAll('input[type="file"]')

  fileInputs.forEach((input) => {
    input.addEventListener("change", function () {
      handleFileUpload(this)
    })
  })
}

/**
 * Handle file upload validation and preview
 */
function handleFileUpload(input) {
  const file = input.files[0]
  const maxSize = 16 * 1024 * 1024 // 16MB

  if (file) {
    // Validate file size
    if (file.size > maxSize) {
      showAlert("File size must be less than 16MB", "danger")
      input.value = ""
      return
    }

    // Validate file type for resume uploads
    if (input.name === "resume") {
      const allowedTypes = ["application/pdf"]
      if (!allowedTypes.includes(file.type)) {
        showAlert("Only PDF files are allowed for resume upload", "danger")
        input.value = ""
        return
      }
    }

    // Show file info
    const fileInfo = document.createElement("div")
    fileInfo.className = "mt-2 text-success"
    fileInfo.innerHTML = `<i class="fas fa-check-circle me-2"></i>Selected: ${file.name} (${formatFileSize(file.size)})`

    // Remove existing file info
    const existingInfo = input.parentNode.querySelector(".file-info")
    if (existingInfo) {
      existingInfo.remove()
    }

    fileInfo.classList.add("file-info")
    input.parentNode.appendChild(fileInfo)
  }
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes"
  const k = 1024
  const sizes = ["Bytes", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
  const anchorLinks = document.querySelectorAll('a[href^="#"]')

  anchorLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href")
      const targetElement = document.querySelector(targetId)

      if (targetElement) {
        e.preventDefault()
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })
}

/**
 * Initialize loading states for forms and buttons
 */
function initializeLoadingStates() {
  const forms = document.querySelectorAll("form")

  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]')
      if (submitBtn) {
        showLoadingState(submitBtn)
      }
    })
  })
}

/**
 * Show loading state on button
 */
function showLoadingState(button) {
  const originalText = button.innerHTML
  button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...'
  button.disabled = true

  // Reset after 10 seconds (fallback)
  setTimeout(() => {
    button.innerHTML = originalText
    button.disabled = false
  }, 10000)
}

/**
 * Initialize auto-dismiss alerts
 */
function initializeAlerts() {
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)")

  alerts.forEach((alert) => {
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      if (alert && alert.parentNode) {
        const bsAlert = new bootstrap.Alert(alert)
        bsAlert.close()
      }
    }, 5000)
  })
}

/**
 * Show custom alert message
 */
function showAlert(message, type = "info") {
  const alertContainer = document.querySelector(".container")
  if (!alertContainer) return

  const alertDiv = document.createElement("div")
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `

  alertContainer.insertBefore(alertDiv, alertContainer.firstChild)

  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    if (alertDiv && alertDiv.parentNode) {
      const bsAlert = new bootstrap.Alert(alertDiv)
      bsAlert.close()
    }
  }, 5000)
}

/**
 * Utility function to format dates
 */
function formatDate(dateString) {
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }
  return new Date(dateString).toLocaleDateString("en-US", options)
}

/**
 * Utility function to debounce function calls
 */
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * Initialize search functionality with debouncing
 */
function initializeSearch() {
  const searchInputs = document.querySelectorAll('input[name="search"]')

  searchInputs.forEach((input) => {
    const debouncedSearch = debounce(() => {
      // Auto-submit form on search input change
      const form = input.closest("form")
      if (form) {
        form.submit()
      }
    }, 500)

    input.addEventListener("input", debouncedSearch)
  })
}

/**
 * Initialize table sorting (if needed)
 */
function initializeTableSorting() {
  const sortableHeaders = document.querySelectorAll("th[data-sort]")

  sortableHeaders.forEach((header) => {
    header.style.cursor = "pointer"
    header.addEventListener("click", function () {
      const table = this.closest("table")
      const column = this.dataset.sort
      sortTable(table, column)
    })
  })
}

/**
 * Sort table by column
 */
function sortTable(table, column) {
  // Basic table sorting implementation
  const tbody = table.querySelector("tbody")
  const rows = Array.from(tbody.querySelectorAll("tr"))

  rows.sort((a, b) => {
    const aValue = a.querySelector(`td[data-${column}]`)?.textContent || ""
    const bValue = b.querySelector(`td[data-${column}]`)?.textContent || ""
    return aValue.localeCompare(bValue)
  })

  rows.forEach((row) => {
    tbody.appendChild(row)
  })
}

/**
 * Initialize copy to clipboard functionality
 */
function initializeClipboard() {
  const copyButtons = document.querySelectorAll("[data-copy]")

  copyButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const textToCopy = this.dataset.copy
      navigator.clipboard.writeText(textToCopy).then(() => {
        showAlert("Copied to clipboard!", "success")
      })
    })
  })
}

// Export functions for use in other scripts
window.EcoTechApp = {
  showAlert,
  formatDate,
  formatFileSize,
  showLoadingState,
  debounce,
}
