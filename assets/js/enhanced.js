/**
 * Enhanced Dynamic JavaScript for Victorine Maikem Portfolio
 * - Typing effect for hero section
 * - Form validation with visual feedback
 * - Counter animations
 * - Scroll progress indicator
 * - Enhanced micro-interactions
 */

(function ($) {
    'use strict';

    // ========================================
    // Scroll Progress Indicator
    // ========================================
    function initScrollProgress() {
        // Create progress element
        if (!$('.scroll-progress').length) {
            $('body').prepend('<div class="scroll-progress"></div>');
        }

        $(window).on('scroll', function () {
            const scrollTop = $(window).scrollTop();
            const docHeight = $(document).height() - $(window).height();
            const scrollPercent = (scrollTop / docHeight) * 100;
            $('.scroll-progress').css('width', scrollPercent + '%');
        });
    }

    // ========================================
    // Typing Effect for Hero
    // ========================================
    function initTypingEffect() {
        const titles = [
            'Digital Health Systems Builder',
            'AI in Healthcare Specialist',
            'Health Informatics Professional',
            'Data Engineering Expert'
        ];

        const heroTitle = $('.basic-details .info h2');
        if (!heroTitle.length) return;

        const originalText = heroTitle.text();
        let currentIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;

        // Add cursor
        if (!heroTitle.find('.typing-cursor').length) {
            heroTitle.append('<span class="typing-cursor"></span>');
        }

        function type() {
            const currentTitle = titles[currentIndex];

            if (isDeleting) {
                heroTitle.contents().first().replaceWith(currentTitle.substring(0, charIndex - 1));
                charIndex--;
                typingSpeed = 50;
            } else {
                heroTitle.contents().first().replaceWith(currentTitle.substring(0, charIndex + 1));
                charIndex++;
                typingSpeed = 100;
            }

            if (!isDeleting && charIndex === currentTitle.length) {
                typingSpeed = 2000; // Pause at end
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                currentIndex = (currentIndex + 1) % titles.length;
                typingSpeed = 500; // Pause before next word
            }

            setTimeout(type, typingSpeed);
        }

        // Start after a delay
        setTimeout(type, 1500);
    }

    // ========================================
    // Enhanced Contact Form
    // ========================================
    function initEnhancedContactForm() {
        const form = $('#contact-form');
        if (!form.length) return;

        // Transform form to enhanced version
        transformContactForm(form);

        // Real-time validation
        form.on('blur', '.floating-label-group input, .floating-label-group textarea', function () {
            validateField($(this));
        });

        form.on('input', '.floating-label-group input, .floating-label-group textarea', function () {
            const group = $(this).closest('.floating-label-group');
            if (group.hasClass('error')) {
                validateField($(this));
            }
        });

        // Enhanced form submission
        form.off('submit').on('submit', function (e) {
            e.preventDefault();

            const btn = form.find('.submit-btn-enhanced');
            const messageDiv = form.find('.form-message-enhanced');
            let isValid = true;

            // Validate all fields
            form.find('.floating-label-group input, .floating-label-group textarea').each(function () {
                if (!validateField($(this))) {
                    isValid = false;
                }
            });

            if (!isValid) {
                showFormMessage(messageDiv, 'error', 'Please correct the errors above.');
                return;
            }

            // Show loading state
            btn.addClass('loading');

            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: form.serialize(),
                success: function (response) {
                    btn.removeClass('loading').addClass('success');
                    btn.find('.btn-text').text('Sent!');
                    showFormMessage(messageDiv, 'success', response.message || 'Thank you! Your message has been sent successfully.');

                    // Reset form after delay
                    setTimeout(function () {
                        form[0].reset();
                        form.find('.floating-label-group').removeClass('success error');
                        btn.removeClass('success');
                        btn.find('.btn-text').text('Send Message');
                        messageDiv.removeClass('show');
                    }, 5000);
                },
                error: function (xhr) {
                    btn.removeClass('loading');
                    const errors = xhr.responseJSON ? xhr.responseJSON.errors : null;
                    showFormMessage(messageDiv, 'error', 'Oops! Something went wrong. Please try again.');

                    if (errors) {
                        Object.keys(errors).forEach(function (field) {
                            const input = form.find('[name="' + field + '"]');
                            const group = input.closest('.floating-label-group');
                            group.addClass('error').removeClass('success');
                            group.find('.error-message').text(errors[field][0]);
                        });
                    }
                }
            });
        });
    }

    function transformContactForm(form) {
        // Wrap form content in enhanced container
        const formContent = form.find('.row');
        if (!formContent.parent().hasClass('contact-form-enhanced')) {
            formContent.wrap('<div class="contact-form-enhanced"></div>');
        }

        // Transform each input to floating label
        form.find('.form-group').each(function () {
            const group = $(this);
            const input = group.find('input, textarea');
            const placeholder = input.attr('placeholder');

            if (!group.hasClass('floating-label-group')) {
                group.addClass('floating-label-group');
                input.attr('placeholder', ' '); // Empty placeholder for CSS

                // Add floating label
                if (!group.find('label').length) {
                    input.after('<label>' + placeholder + '</label>');
                }

                // Add validation icon
                if (!group.find('.validation-icon').length) {
                    input.after('<span class="validation-icon"><i class="fa-solid fa-check"></i></span>');
                }

                // Add error message container
                if (!group.find('.error-message').length) {
                    group.append('<span class="error-message"></span>');
                }
            }
        });

        // Transform submit button
        const submitBtn = form.find('button[type="submit"]');
        if (!submitBtn.hasClass('submit-btn-enhanced')) {
            submitBtn.addClass('submit-btn-enhanced').removeClass('custom-btn bx-btn-1');
            const btnText = submitBtn.text();
            submitBtn.html(`
                <span class="btn-text">${btnText}</span>
                <span class="btn-loader"><div class="spinner"></div></span>
                <i class="fa-solid fa-paper-plane"></i>
            `);
        }

        // Add/update form message container
        if (!form.find('.form-message-enhanced').length) {
            form.append('<div class="form-message-enhanced"><span class="message-icon"></span><span class="message-text"></span></div>');
        }
    }

    function validateField(input) {
        const group = input.closest('.floating-label-group');
        const value = input.val().trim();
        const name = input.attr('name') || input.attr('id');
        let isValid = true;
        let errorMsg = '';

        // Required validation
        if (!value) {
            isValid = false;
            errorMsg = 'This field is required';
        }

        // Email validation
        if (isValid && (name === 'email' || input.attr('type') === 'email')) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMsg = 'Please enter a valid email address';
            }
        }

        // Phone validation (optional field, validate format if provided)
        if (isValid && name === 'phone' && value) {
            const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                errorMsg = 'Please enter a valid phone number';
            }
        }

        // Update UI
        if (isValid) {
            group.removeClass('error').addClass('success');
            group.find('.validation-icon i').removeClass('fa-times').addClass('fa-check');
        } else {
            group.removeClass('success').addClass('error');
            group.find('.validation-icon i').removeClass('fa-check').addClass('fa-times');
            group.find('.error-message').text(errorMsg);
        }

        return isValid;
    }

    function showFormMessage(container, type, message) {
        const icon = type === 'success' ? '<i class="fa-solid fa-circle-check"></i>' : '<i class="fa-solid fa-circle-exclamation"></i>';
        container.removeClass('success error').addClass(type + ' show');
        container.find('.message-icon').html(icon);
        container.find('.message-text').text(message);
    }

    // ========================================
    // Counter Animation
    // ========================================
    function initCounterAnimation() {
        const counters = document.querySelectorAll('[data-counter]');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    }

    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-counter'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                element.textContent = target + (element.getAttribute('data-suffix') || '');
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current) + (element.getAttribute('data-suffix') || '');
            }
        }, 16);
    }

    // ========================================
    // Enhanced Service Cards
    // ========================================
    function initServiceCards() {
        $('.section-card').each(function (index) {
            $(this).css('animation-delay', (index * 0.1) + 's');
        });
    }

    // ========================================
    // Smooth Section Reveal
    // ========================================
    function initSectionReveal() {
        const sections = document.querySelectorAll('.bx-section');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('section-visible');
                }
            });
        }, { threshold: 0.1 });

        sections.forEach(section => {
            section.classList.add('section-hidden');
            observer.observe(section);
        });
    }

    // ========================================
    // Portfolio Filter Enhancement
    // ========================================
    function initPortfolioFilter() {
        $('.portfolio-tabs .filter').on('click', function () {
            const $this = $(this);

            // Add active animation
            $('.portfolio-tabs .filter').removeClass('active-filter');
            $this.addClass('active-filter');

            // Animate items
            $('.portfolio-content-items .mix').each(function (index) {
                $(this).css({
                    'animation-delay': (index * 0.05) + 's',
                    'animation-name': 'fadeInUp'
                });
            });
        });
    }

    // ========================================
    // Navbar scroll effect
    // ========================================
    function initNavbarScroll() {
        $(window).on('scroll', function () {
            if ($(window).scrollTop() > 100) {
                $('header').addClass('scrolled');
            } else {
                $('header').removeClass('scrolled');
            }
        });
    }

    // ========================================
    // Initialize all enhancements
    // ========================================
    $(document).ready(function () {
        initScrollProgress();
        initTypingEffect();
        initEnhancedContactForm();
        initCounterAnimation();
        initServiceCards();
        initSectionReveal();
        initPortfolioFilter();
        initNavbarScroll();

        // Add pulse animation to CTA buttons
        $('.bx-btn').addClass('pulse-animation');

        console.log('✨ Enhanced dynamic features initialized');
    });

})(jQuery);
