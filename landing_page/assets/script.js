// Redirect to waitlist page function (must be global for inline onclick)
function redirectToWaitlistPage() {
    const qualifyInput = document.getElementById('qualifyInput');
    const val = (qualifyInput && qualifyInput.value || '').trim();
    if (val) {
        const encodedAddress = encodeURIComponent(val);
        window.location.href = `join-waitlist.html?address=${encodedAddress}`;
    } else {
        window.location.href = 'join-waitlist.html';
    }
    return false;
}

// Dynamic Counter Animation
function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000; // 2 seconds
    const increment = target / (duration / 16); // 60fps
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// Intersection Observer for counter animation
const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px'
};

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.dataset.animated) {
            entry.target.dataset.animated = 'true';
            animateCounter(entry.target);
        }
    });
}, observerOptions);

// Pricing Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize counter observers
    const counters = document.querySelectorAll('.metric-counter');
    if (counters.length > 0) {
        counters.forEach(counter => {
            counterObserver.observe(counter);
            // Also check if already in view on load
            const rect = counter.getBoundingClientRect();
            const isInView = rect.top < window.innerHeight && rect.bottom > 0;
            if (isInView && !counter.dataset.animated) {
                counter.dataset.animated = 'true';
                animateCounter(counter);
            }
        });
    }
    // Pricing Toggle Functionality (fixed)
    const toggleButtons = document.querySelectorAll('.pricing-toggle .toggle-btn');

    // If setPhase exists (defined below the pricing calculator), clicking a toggle will switch phases
    function safeSetPhase(p) {
        if (typeof setPhase === 'function') {
            setPhase(p);
        }
    }

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const phase = this.getAttribute('data-phase'); // "p1" | "p2" | "p3"

            // Button active state
            toggleButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Drive the calculator UI
            safeSetPhase(phase);
        });
    });
    
    // Pricing Calculator
    const monthlyBillInput = document.getElementById('monthlyBill');
    const planTypeSelect = document.getElementById('planType');
    const monthlySavingsSpan = document.getElementById('monthlySavings');
    const annualSavingsSpan = document.getElementById('annualSavings');
    const paybackPeriodSpan = document.getElementById('paybackPeriod');
    const tenYearSavingsSpan = document.getElementById('tenYearSavings');
    
    function calculatePricingSavings() {
        const monthlyBill = parseFloat(monthlyBillInput.value) || 0;
        const planType = planTypeSelect.value;
        
        if (monthlyBill === 0) {
            monthlySavingsSpan.textContent = '$0';
            annualSavingsSpan.textContent = '$0';
            paybackPeriodSpan.textContent = '0 months';
            tenYearSavingsSpan.textContent = '$0';
            return;
        }
        
        // Define savings percentages by membership type (Base Power model)
        const savingsRates = {
            residential: 0.20, // 20% average savings
            business: 0.25,    // 25% average savings
            enterprise: 0.30  // 30% average savings
        };
        
        const savingsRate = savingsRates[planType];
        const monthlySavings = monthlyBill * savingsRate;
        const annualSavings = monthlySavings * 12;
        const tenYearSavings = annualSavings * 10;
        
        // Calculate payback period (assuming upfront cost of 1 month's bill)
        const upfrontCost = monthlyBill;
        const paybackMonths = Math.ceil(upfrontCost / monthlySavings);
        
        monthlySavingsSpan.textContent = '$' + monthlySavings.toFixed(2);
        annualSavingsSpan.textContent = '$' + annualSavings.toFixed(2);
        paybackPeriodSpan.textContent = paybackMonths + ' months';
        tenYearSavingsSpan.textContent = '$' + tenYearSavings.toFixed(0);
    }
    
    monthlyBillInput.addEventListener('input', calculatePricingSavings);
    planTypeSelect.addEventListener('change', calculatePricingSavings);
    
    // Initialize calculator
    calculatePricingSavings();
});

// Problem Carousel Functionality
let currentProblemIndex = 1;
const totalProblems = 5;

function changeProblem(direction) {
    const problemCards = document.querySelectorAll('.problem-card');
    const dots = document.querySelectorAll('.problem-dots .dot');
    
    // Remove active class from current card and dot
    problemCards[currentProblemIndex - 1].classList.remove('active');
    dots[currentProblemIndex - 1].classList.remove('active');
    
    // Calculate new index
    currentProblemIndex += direction;
    
    // Handle wrapping
    if (currentProblemIndex > totalProblems) {
        currentProblemIndex = 1;
    } else if (currentProblemIndex < 1) {
        currentProblemIndex = totalProblems;
    }
    
    // Add active class to new card and dot
    problemCards[currentProblemIndex - 1].classList.add('active');
    dots[currentProblemIndex - 1].classList.add('active');
    
    // Update navigation buttons
    updateNavButtons();
}

function currentProblem(index) {
    const problemCards = document.querySelectorAll('.problem-card');
    const dots = document.querySelectorAll('.problem-dots .dot');
    
    // Remove active class from all cards and dots
    problemCards.forEach(card => card.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    // Set new current index
    currentProblemIndex = index;
    
    // Add active class to selected card and dot
    problemCards[currentProblemIndex - 1].classList.add('active');
    dots[currentProblemIndex - 1].classList.add('active');
    
    // Update navigation buttons
    updateNavButtons();
}

function updateNavButtons() {
    const prevBtn = document.querySelector('.problem-nav .prev');
    const nextBtn = document.querySelector('.problem-nav .next');
    
    // Enable/disable buttons based on current position
    prevBtn.disabled = false;
    nextBtn.disabled = false;
}

// Initialize problem carousel
document.addEventListener('DOMContentLoaded', function() {
    // Manual navigation only - no auto-advance
});

// Interactive Features for AsphaltToEnergy Website

document.addEventListener('DOMContentLoaded', function() {
    // Savings Calculator
    const powerBillInput = document.getElementById('powerBill');
    const savingsRangeInput = document.getElementById('savingsRange');
    const savingsValueSpan = document.getElementById('savingsValue');
    const monthlySavingsSpan = document.getElementById('monthlySavings');
    const reservedSolarSpan = document.getElementById('reservedSolar');
    const energyProducedSpan = document.getElementById('energyProduced');
    const annualSavingsSpan = document.getElementById('annualSavings');
    const tenYearSavingsSpan = document.getElementById('tenYearSavings');
    const reservationFeeSpan = document.getElementById('reservationFee');

    // Update savings range display
    savingsRangeInput.addEventListener('input', function() {
        savingsValueSpan.textContent = this.value + '%';
        calculateSavings();
    });

    // Calculate savings when power bill changes
    powerBillInput.addEventListener('input', calculateSavings);

    function calculateSavings() {
        const powerBill = parseFloat(powerBillInput.value) || 0;
        const savingsPercentage = parseFloat(savingsRangeInput.value) || 75;
        
        if (powerBill === 0) {
            // Reset all values
            monthlySavingsSpan.textContent = '---';
            reservedSolarSpan.textContent = '---';
            energyProducedSpan.textContent = '--- kWh';
            annualSavingsSpan.textContent = '---';
            tenYearSavingsSpan.textContent = '---';
            reservationFeeSpan.textContent = '---';
            return;
        }

        // Calculate savings based on parking lot solar economics
        const monthlySavings = (powerBill * savingsPercentage / 100);
        const annualSavings = monthlySavings * 12;
        const tenYearSavings = annualSavings * 10;
        
        // Estimate solar capacity needed (rough calculation)
        // Assuming $0.12/kWh average electricity cost
        const avgElectricityCost = 0.12;
        const monthlyKWh = powerBill / avgElectricityCost;
        const solarCapacityNeeded = (monthlyKWh * 12) / (1200); // Assuming 1200 kWh/kW/year
        
        // Energy produced per month
        const energyProduced = solarCapacityNeeded * 100; // Rough estimate
        
        // Reservation fee (one-time cost)
        const reservationFee = solarCapacityNeeded * 2500; // $2500 per kW reservation fee
        
        // Update display
        monthlySavingsSpan.textContent = '$' + monthlySavings.toFixed(2);
        reservedSolarSpan.textContent = solarCapacityNeeded.toFixed(1) + ' kW';
        energyProducedSpan.textContent = energyProduced.toFixed(0) + ' kWh';
        annualSavingsSpan.textContent = '$' + annualSavings.toFixed(2);
        tenYearSavingsSpan.textContent = '$' + tenYearSavings.toFixed(2);
        reservationFeeSpan.textContent = '$' + reservationFee.toFixed(0);
    }

    // FAQ Tabs
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Challenges & Solutions Section
    const challengeButtons = document.querySelectorAll('.challenge-filters .filter-btn');
    const challengeCards = document.querySelectorAll('.challenge-list .challenge-card');
    
    if (challengeButtons.length > 0 && challengeCards.length > 0) {
        challengeButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all buttons
                challengeButtons.forEach(b => { 
                    b.classList.remove('active'); 
                    b.setAttribute('aria-selected', 'false'); 
                });
                
                // Add active class to clicked button
                btn.classList.add('active'); 
                btn.setAttribute('aria-selected', 'true');
                
                // Get filter value
                const filterValue = btn.getAttribute('data-filter');
                
                // Filter cards
                challengeCards.forEach(card => {
                    const cardCategory = card.getAttribute('data-cat');
                    if (filterValue === 'all' || cardCategory === filterValue) {
                        card.style.display = '';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
        
        // Expand/Collapse all buttons
        const expandBtn = document.getElementById('expandAll');
        const collapseBtn = document.getElementById('collapseAll');
        
        if (expandBtn) {
            expandBtn.addEventListener('click', function(e) {
                e.preventDefault();
                challengeCards.forEach(card => card.open = true);
            });
        }
        
        if (collapseBtn) {
            collapseBtn.addEventListener('click', function(e) {
                e.preventDefault();
                challengeCards.forEach(card => card.open = false);
            });
        }
    }

    // Animate stats on scroll
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };

    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStats();
                statsObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }

    function animateStats() {
        const statValues = document.querySelectorAll('.stat-value');
        
        statValues.forEach(stat => {
            const finalValue = stat.textContent;
            const numericValue = parseFloat(finalValue.replace(/[^\d.]/g, ''));
            
            if (!isNaN(numericValue)) {
                animateNumber(stat, 0, numericValue, 2000, finalValue);
            }
        });
    }

    function animateNumber(element, start, end, duration, originalText) {
        const startTime = performance.now();
        const isCurrency = originalText.includes('$');
        const isKWh = originalText.includes('kWh');
        const isKg = originalText.includes('kg');
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = start + (end - start) * easeOutQuart;
            
            let displayValue = currentValue.toFixed(1);
            
            // Format based on original text
            if (isCurrency) {
                element.textContent = '$' + displayValue;
            } else if (isKWh) {
                element.textContent = displayValue + ' kWh';
            } else if (isKg) {
                element.textContent = displayValue + ' kg';
            } else {
                element.textContent = displayValue;
            }
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            } else {
                element.textContent = originalText;
            }
        }
        
        requestAnimationFrame(updateNumber);
    }

    // Add hover effects to feature cards
    const featureCards = document.querySelectorAll('.feature-card, .benefit-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Form validation for calculator
    powerBillInput.addEventListener('blur', function() {
        const value = parseFloat(this.value);
        if (value < 50) {
            this.style.borderColor = '#DC3545';
            this.setCustomValidity('Minimum power bill should be $50');
        } else if (value > 1000) {
            this.style.borderColor = '#DC3545';
            this.setCustomValidity('Maximum power bill should be $1000');
        } else {
            this.style.borderColor = '#E0E0E0';
            this.setCustomValidity('');
        }
    });

    // Add loading animation for buttons
    const primaryButtons = document.querySelectorAll('.btn-primary');
    primaryButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.textContent;
            this.textContent = 'Loading...';
            this.disabled = true;
            
            // Simulate loading (remove this in production)
            setTimeout(() => {
                this.textContent = originalText;
                this.disabled = false;
            }, 2000);
        });
    });

    // Initialize calculator with default values
    calculateSavings();
    
    // Before/After Slider
    const baContainer = document.querySelector('.ba-container');
    const baBefore = document.querySelector('.ba-before');
    const baHandle = document.querySelector('.ba-handle');
    
    if (baContainer && baBefore && baHandle) {
        let isDragging = false;
        let currentPosition = 50; // Start at 50%
        
        function updateSlider(clientX) {
            const rect = baContainer.getBoundingClientRect();
            const x = clientX - rect.left;
            const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
            currentPosition = percentage;
            
            baBefore.style.width = percentage + '%';
            baHandle.style.left = percentage + '%';
        }
        
        function startDrag(e) {
            isDragging = true;
            const clientX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
            updateSlider(clientX);
            e.preventDefault();
        }
        
        function drag(e) {
            if (!isDragging) return;
            const clientX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
            updateSlider(clientX);
            e.preventDefault();
        }
        
        function stopDrag() {
            isDragging = false;
        }
        
        // Mouse events
        baContainer.addEventListener('mousedown', startDrag);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', stopDrag);
        
        // Also make handle draggable
        baHandle.addEventListener('mousedown', startDrag);
        
        // Touch support
        baContainer.addEventListener('touchstart', startDrag, { passive: false });
        document.addEventListener('touchmove', drag, { passive: false });
        document.addEventListener('touchend', stopDrag);
        
        // Initialize position
        baBefore.style.width = currentPosition + '%';
        baHandle.style.left = currentPosition + '%';
    }
    
    // Role Carousel
    const roleButtons = document.querySelectorAll('.role-btn');
    const ctaBtn = document.getElementById('ctaBtn');
    
    console.log('Role buttons found:', roleButtons.length);
    console.log('CTA button found:', ctaBtn);
    
    const roleTexts = {
        host: 'Become a Host',
        investor: 'Invest Now',
        partner: 'Partner With Us'
    };
    
    if (roleButtons.length > 0) {
        roleButtons.forEach((btn, index) => {
            console.log('Adding listener to button:', index, btn);
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Button clicked:', this.getAttribute('data-role'));
                
                // Remove active class from all buttons
                roleButtons.forEach(b => b.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');
                
                // Update CTA button text
                const role = this.getAttribute('data-role');
                console.log('Role:', role, 'Text:', roleTexts[role]);
                if (ctaBtn && roleTexts[role]) {
                    ctaBtn.textContent = roleTexts[role];
                    console.log('Updated CTA button to:', roleTexts[role]);
                }
            });
        });
    } else {
        console.error('No role buttons found!');
    }
    
    // Interactive Dashboard Preview
    const dashboardMockup = document.getElementById('dashboardMockup');
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    
    if (dashboardMockup && dashboardCards.length > 0) {
        // Animate values on hover
        dashboardMockup.addEventListener('mouseenter', function() {
            dashboardCards.forEach(card => {
                const valueEl = card.querySelector('.card-value');
                const target = valueEl.getAttribute('data-target');
                const metric = card.getAttribute('data-metric');
                
                if (valueEl && target) {
                    const currentValue = parseFloat(valueEl.textContent.replace(/[^0-9.]/g, '')) || 0;
                    const targetValue = parseFloat(target);
                    
                    // Animate to target value
                    animateDashboardValue(valueEl, currentValue, targetValue, metric);
                }
            });
        });
        
        // Reset values on mouse leave
        dashboardMockup.addEventListener('mouseleave', function() {
            dashboardCards.forEach(card => {
                const valueEl = card.querySelector('.card-value');
                const target = valueEl.getAttribute('data-target');
                const metric = card.getAttribute('data-metric');
                
                if (valueEl && target) {
                    const targetValue = parseFloat(target);
                    const currentValue = parseFloat(valueEl.textContent.replace(/[^0-9.]/g, '')) || 0;
                    
                    // Animate back to initial value
                    animateDashboardValue(valueEl, currentValue, 0, metric);
                }
            });
        });
        
        // Function to animate dashboard values
        function animateDashboardValue(element, start, end, metric) {
            const duration = 1000;
            const startTime = performance.now();
            const isCurrency = metric === 'savings';
            const isDecimal = metric === 'co2';
            
            function updateValue(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing function
                const easeOutCubic = 1 - Math.pow(1 - progress, 3);
                const currentValue = start + (end - start) * easeOutCubic;
                
                // Format based on metric type
                if (isCurrency) {
                    element.textContent = '$' + Math.floor(currentValue).toLocaleString();
                } else if (isDecimal) {
                    element.textContent = currentValue.toFixed(1);
                } else {
                    element.textContent = Math.floor(currentValue).toLocaleString();
                }
                
                if (progress < 1) {
                    requestAnimationFrame(updateValue);
                } else {
                    // Ensure final value is exact
                    if (isCurrency) {
                        element.textContent = '$' + Math.floor(end).toLocaleString();
                    } else if (isDecimal) {
                        element.textContent = end.toFixed(1);
                    } else {
                        element.textContent = Math.floor(end).toLocaleString();
                    }
                }
            }
            
            requestAnimationFrame(updateValue);
        }
        
        // Initialize with zero values
        dashboardCards.forEach(card => {
            const valueEl = card.querySelector('.card-value');
            const metric = card.getAttribute('data-metric');
            
            if (valueEl) {
                if (metric === 'savings') {
                    valueEl.textContent = '$0';
                } else if (metric === 'co2') {
                    valueEl.textContent = '0.0';
                } else {
                    valueEl.textContent = '0';
                }
            }
        });
    }
    
    // Modal Functionality
    const joinProjectsBtn = document.getElementById('joinProjectsBtn');
    const talkToUsBtn = document.getElementById('talkToUsBtn');
    const footerTalkToUs = document.getElementById('footerTalkToUs');
    const checkQualifyBtn = document.getElementById('checkQualifyBtn');
    const qualifyInput = document.getElementById('qualifyInput');
    const hostModal = document.getElementById('hostModal');
    const earlyAccessModal = document.getElementById('earlyAccessModal');
    const closeHostModal = document.getElementById('closeHostModal');
    const closeEarlyAccessModal = document.getElementById('closeEarlyAccessModal');
    
    // Open Host Modal
    if (joinProjectsBtn && hostModal) {
        joinProjectsBtn.addEventListener('click', () => {
            hostModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }
    
    // Open Early Access Modal from Talk to Us button
    if (talkToUsBtn && earlyAccessModal) {
        talkToUsBtn.addEventListener('click', () => {
            earlyAccessModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }
    // Open Early Access Modal from footer link
    if (footerTalkToUs && earlyAccessModal) {
        footerTalkToUs.addEventListener('click', (e) => {
            e.preventDefault();
            earlyAccessModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    // Qualify check → redirect to waitlist page with address
    function redirectToWaitlist() {
        const val = (qualifyInput && qualifyInput.value || '').trim();
        if (val) {
            // Encode the address and redirect to waitlist page
            const encodedAddress = encodeURIComponent(val);
            window.location.href = `join-waitlist.html?address=${encodedAddress}`;
        } else {
            // If no address entered, just go to waitlist page
            window.location.href = 'join-waitlist.html';
        }
    }

    if (checkQualifyBtn) {
        checkQualifyBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            redirectToWaitlist();
        });
    }
    
    if (qualifyInput) {
        qualifyInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                e.stopPropagation();
                redirectToWaitlist();
            }
        });
    }
    
    // Open Early Access Modal from CTA button (when set to "Get Early Access")
    if (ctaBtn && earlyAccessModal) {
        ctaBtn.addEventListener('click', () => {
            const btnText = ctaBtn.textContent.toLowerCase();
            if (btnText.includes('early') || btnText === 'get started') {
                earlyAccessModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            } else if (btnText.includes('host') || btnText.includes('become')) {
                hostModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    }
    
    // Close Host Modal
    if (closeHostModal && hostModal) {
        closeHostModal.addEventListener('click', () => {
            hostModal.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // Close Early Access Modal
    if (closeEarlyAccessModal && earlyAccessModal) {
        closeEarlyAccessModal.addEventListener('click', () => {
            earlyAccessModal.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // Close modals when clicking overlay
    if (hostModal) {
        hostModal.addEventListener('click', (e) => {
            if (e.target === hostModal || e.target.classList.contains('modal-overlay')) {
                hostModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    if (earlyAccessModal) {
        earlyAccessModal.addEventListener('click', (e) => {
            if (e.target === earlyAccessModal || e.target.classList.contains('modal-overlay')) {
                earlyAccessModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    // Close modals on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (hostModal && hostModal.classList.contains('active')) {
                hostModal.classList.remove('active');
                document.body.style.overflow = '';
            }
            if (earlyAccessModal && earlyAccessModal.classList.contains('active')) {
                earlyAccessModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
    });
    
    // Form Submission Handlers
    const hostForm = document.getElementById('hostForm');
    const earlyAccessForm = document.getElementById('earlyAccessForm');
    
    if (hostForm) {
        hostForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show success message
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Submitting...';
            submitBtn.disabled = true;
            
            // Submit to Google Forms (form will submit in background)
            // Note: Update the form action URL with your actual Google Form ID
            // and update all entry.xxxxx with your actual field entry IDs
            
            // Simulate form submission (Google Forms will handle this)
            setTimeout(() => {
                submitBtn.textContent = 'Request Submitted! ✓';
                setTimeout(() => {
                    hostModal.classList.remove('active');
                    document.body.style.overflow = '';
                    this.reset();
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }, 1500);
            }, 1000);
            
            // Actually submit to Google Forms
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                mode: 'no-cors'
            }).catch(() => {
                // Google Forms doesn't return CORS headers, so this will fail silently
                // but the form will still submit
            });
        });
    }
    
    if (earlyAccessForm) {
        earlyAccessForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show success message
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Submitting...';
            submitBtn.disabled = true;
            
            // Simulate form submission
            setTimeout(() => {
                submitBtn.textContent = 'Joined Waitlist! ✓';
                setTimeout(() => {
                    earlyAccessModal.classList.remove('active');
                    document.body.style.overflow = '';
                    this.reset();
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }, 1500);
            }, 1000);
            
            // Actually submit to Google Forms
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                mode: 'no-cors'
            }).catch(() => {
                // Google Forms doesn't return CORS headers, so this will fail silently
                // but the form will still submit
            });
        });
    }
    
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

// Add scroll-to-top functionality
window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 300) {
        // Show scroll to top button (you can add this button to HTML)
        const scrollToTopBtn = document.getElementById('scrollToTop');
        if (scrollToTopBtn) {
            scrollToTopBtn.style.display = 'block';
        }
    } else {
        const scrollToTopBtn = document.getElementById('scrollToTop');
        if (scrollToTopBtn) {
            scrollToTopBtn.style.display = 'none';
        }
    }
});

// Add scroll to top button functionality
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// ============================================
// PWA - Service Worker Registration
// ============================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then((registration) => {
                console.log('Service Worker registered successfully:', registration.scope);
                
                // Check for updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // New service worker available
                            showUpdateNotification();
                        }
                    });
                });
            })
            .catch((error) => {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// ============================================
// PWA - Install Prompt
// ============================================

let deferredPrompt;
const installButton = document.getElementById('installAppBtn');

// Listen for the beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;
    // Show install button if it exists
    if (installButton) {
        installButton.style.display = 'block';
    } else {
        // Create install button if it doesn't exist
        createInstallButton();
    }
});

// Create install button dynamically
function createInstallButton() {
    const installBtn = document.createElement('button');
    installBtn.id = 'installAppBtn';
    installBtn.className = 'btn-primary';
    installBtn.innerHTML = '<i class="fas fa-download"></i> Install App';
    installBtn.style.display = 'none';
    installBtn.style.position = 'fixed';
    installBtn.style.bottom = '20px';
    installBtn.style.right = '20px';
    installBtn.style.zIndex = '10000';
    installBtn.style.borderRadius = '50px';
    installBtn.style.padding = '12px 24px';
    installBtn.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    
    installBtn.addEventListener('click', async () => {
        if (!deferredPrompt) {
            return;
        }
        
        // Show the install prompt
        deferredPrompt.prompt();
        
        // Wait for the user to respond to the prompt
        const { outcome } = await deferredPrompt.userChoice;
        
        if (outcome === 'accepted') {
            console.log('User accepted the install prompt');
        } else {
            console.log('User dismissed the install prompt');
        }
        
        // Clear the deferredPrompt
        deferredPrompt = null;
        installBtn.style.display = 'none';
    });
    
    document.body.appendChild(installBtn);
}

// Listen for app installed event
window.addEventListener('appinstalled', () => {
    console.log('PWA was installed');
    deferredPrompt = null;
    if (installButton) {
        installButton.style.display = 'none';
    }
    // Show success message
    showNotification('App installed successfully!', 'success');
});

// ============================================
// PWA - Update Notification
// ============================================

function showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'pwa-update-notification';
    notification.innerHTML = `
        <div style="background: var(--primary-orange); color: white; padding: 1rem; border-radius: 8px; margin: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <p style="margin: 0 0 0.5rem 0; font-weight: 600;">New version available!</p>
            <button onclick="window.location.reload()" style="background: white; color: var(--primary-orange); border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: 600;">
                Update Now
            </button>
        </div>
    `;
    notification.style.position = 'fixed';
    notification.style.top = '80px';
    notification.style.left = '50%';
    notification.style.transform = 'translateX(-50%)';
    notification.style.zIndex = '10001';
    notification.style.maxWidth = '400px';
    notification.style.width = '90%';
    
    document.body.appendChild(notification);
    
    // Auto-dismiss after 10 seconds
    setTimeout(() => {
        notification.remove();
    }, 10000);
}

// ============================================
// PWA - Notification Helper
// ============================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'pwa-notification';
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10002;
        max-width: 400px;
        width: 90%;
        animation: slideUp 0.3s ease;
    `;
    notification.textContent = message;
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            from {
                transform: translateX(-50%) translateY(100px);
                opacity: 0;
            }
            to {
                transform: translateX(-50%) translateY(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideUp 0.3s ease reverse';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ============================================
// PWA - Offline Detection
// ============================================

window.addEventListener('online', () => {
    showNotification('You are back online!', 'success');
});

window.addEventListener('offline', () => {
    showNotification('You are offline. Some features may be limited.', 'info');
});
