;;;;; MELPA PACKAGE ;;;;;
(require 'package)
(let* ((no-ssl (and (memq system-type '(windows-nt ms-dos))
                    (not (gnutls-available-p))))
       (proto (if no-ssl "http" "http")))
       ;; (proto (if no-ssl "http" "https")))
  (when no-ssl
    (warn "\
Your version of Emacs does not support SSL connections,
which is unsafe because it allows man-in-the-middle attacks.
There are two things you can do about this warning:
1. Install an Emacs version that does support SSL and be safe.
2. Remove this warning from your init file so you won't see it again."))
  ;; Comment/uncomment these two lines to enable/disable MELPA and MELPA Stable as desired
  (add-to-list 'package-archives (cons "melpa" (concat proto "://melpa.org/packages/")) t)
  ;;(add-to-list 'package-archives (cons "melpa-stable" (concat proto "://stable.melpa.org/packages/")) t)
  (when (< emacs-major-version 24)
    ;; For important compatibility libraries like cl-lib
    (add-to-list 'package-archives (cons "gnu" (concat proto "://elpa.gnu.org/packages/")))))
(package-initialize)
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-safe-themes
   (quote
    ("a2cde79e4cc8dc9a03e7d9a42fabf8928720d420034b66aecc5b665bbf05d4e9" default)))
 '(package-check-signature (quote allow-unsigned))
 '(package-selected-packages
   (quote
    (py-autopep8 projectile company poly-R polymode markdown-mode dockerfile-mode flycheck conda elpy helm-projectile helm-company swiper ess-R-data-view helm avy expand-region rainbow-delimiters general use-package monokai-theme ess-view gnu-elpa-keyring-update ess))))

(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )

;; ========== General =========
(load-theme 'monokai)

;; Some configurations below require this

;; wrapper for keybindinds
(require 'use-package)

;; a simple way to manage simple keybindings
(require 'general)

;; Inhibit initial emacs screen: C-h C-a
(setq inhibit-startup-screen t)

;; Disable menu bar
(tool-bar-mode -1)

;; Disable scrollbar
(toggle-scroll-bar -1)

;; Show line numbers
(add-hook 'prog-mode-hook 'linum-mode)
(add-hook 'latex-mode-hook 'linum-mode)

;; Show and highlight the corresponding parenthesis
(require 'paren)
(show-paren-mode)

; Rainbow delimiters
(add-hook 'prog-mode-hook #'rainbow-delimiters-mode)

;; Expand-region
(require 'expand-region)
(global-set-key (kbd "C-*") 'er/expand-region)

;; Avy
;; Jump to line using two characters
(global-set-key (kbd "C-c SPC") 'avy-goto-char-timer)


; Disable pinging
(setq ffap-machine-p-known 'reject)

;; ========== LaTeX ==========
(setq latex-run-command "pdflatex")

;; ========== Window management =========
;; Move within windows using the META key (ALT)
(windmove-default-keybindings 'meta)

;; ========== ESS =========
;; Make ess-describe buffer always display on the right side
(setq display-buffer-alist
      `(("*ess-describe*"
         (display-buffer-reuse-window display-buffer-in-side-window)
         (side . right)
         (slot . 1)
         (window-width . 0.5)
         (reusable-frames . nil))))


;; Use RMarkdown with polymode and poly-markdown
(require 'polymode)
(require 'poly-markdown)
(require 'poly-R)

;; Sends the input to the iESS buffer but does not wait for the process to finish
;; ensuring Emacs is not blocked. http://ess.r-project.org/Manual/ess.html
(setq ess-eval-visibly 'nowait)

;; Disable comment indent in ESS
(setq ess-fancy-comments nil)

;; Custom functions
(defun dotted-symbol-at-point ()
  (with-syntax-table (make-syntax-table (syntax-table))
    (modify-syntax-entry ?. "_")
    (thing-at-point 'symbol)))

(defun pipe_R_operator ()
  "R - %>% operator or pipe operator"
  (interactive)
  (just-one-space 1)
  (insert "%>%")
  (just-one-space 1))

(defun ess-head ()
  "Head n=10 of object"
  (interactive)
  (ess-execute (concat "head(" (dotted-symbol-at-point) ", n=10)\n") t))

(defun ess-tail ()
  "Tail n=10 of object"
  (interactive)
  (ess-execute (concat "tail(" (dotted-symbol-at-point) ", n=10)\n") t))

(defun ess-upper-square ()
  "X[1:5, 1:5]"
  (interactive)
  (ess-execute (concat (dotted-symbol-at-point) "[1:5, 1:5]\n") t))

(defun ess-dim ()
  "dim(X)"
  (interactive)
  (ess-execute (concat "dim(" (dotted-symbol-at-point) ")\n") t))

(defun ess-rownames ()
  "rownames(X)"
  (interactive)
  (ess-execute (concat "rownames(" (dotted-symbol-at-point) ")\n") t))

(defun ess-colnames ()
  "colnames(X)"
  (interactive)
  (ess-execute (concat "colnames(" (dotted-symbol-at-point) ")\n") t))

(defun ess-view ()
  "View(X)"
  (interactive)
  (ess-execute (concat "View(" (dotted-symbol-at-point) ")\n") t))

(defun ess-in ()
  "R %in% operator"
  (interactive)
  (just-one-space 1)
  (insert "%in%")
  (just-one-space 1))

(defun ess-ls ()
  "ls()"
  (interactive)
  (ess-execute "ls()\n" t))

;; (defun ess-length ()
;;   "length(x)"
;;   (interactive)
;;   (ess-execute (concat "length(" (dotted-symbol-at-point) ")\n") t))

;; Smart assignment cycling with C-;
;; Pipe with C-ñ
(use-package ess-mode
  :bind
  (:map ess-mode-map
        ("C-;" . ess-cycle-assign)
	("C-ñ" . 'pipe_R_operator)
	("C-c h" . 'ess-head)
	("C-c t" . 'ess-tail)
	("C-c u" . 'ess-upper-square)
	("C-c d" . 'ess-dim)
	("C-c r" . 'ess-rownames)
	("C-c c" . 'ess-colnames)
	("C-c v" . 'ess-view)
	("C-c i" . 'ess-in)
	("C-c l" . 'ess-ls)
	)
  (:map inferior-ess-mode-map
	("C-;" . ess-cycle-assign)
	("C-ñ" . 'pipe_R_operator)
	("C-c h" . 'ess-head)
	("C-c t" . 'ess-tail)
	("C-c u" . 'ess-upper-square)
	("C-c d" . 'ess-dim)
	("C-c r" . 'ess-rownames)
	("C-c c" . 'ess-colnames)
	("C-c v" . 'ess-view)
	("C-c i" . 'ess-in)
	("C-c l" . 'ess-ls)))

;; Disable flymake
(setq ess-use-flymake nil)

;; ==========  ESS-company =========
;; Company is a modular completion framework 
;; Use company mode in all buffers 
;; and turn off tooltips
(use-package company
  :ensure t
  :config (setq company-frontends nil)
  :init (add-hook 'after-init-hook 'global-company-mode))

;; Recommended settings for company
(setq ess-use-company t
      company-selection-wrap-around t
      company-tooltip-align-annotations t
      company-idle-delay 0.36
      company-minimum-prefix-length 2
      company-tooltip-limit 10)

;; Necessary to have auto-complete for completion in scripts
(setq ess-tab-complete-in-script t)

; Changing default keys for movement
(with-eval-after-load 'company
  (define-key company-active-map (kbd "M-¡") 'company-show-doc-buffer)
  (define-key company-active-map [return] nil)
  (define-key company-active-map (kbd "M-TAB") 'company-complete-common)
  (define-key company-active-map (kbd "M-TAB") 'company-complete-selection))

;; ======= Helm =======
;; Helm is an Emacs incremental and narrowing framework
;; It helps to rapidly complete file names, buffer names 

(require 'helm)
(require 'helm-config)

;; The default "C-x c" is quite close to "C-x C-c", which quits Emacs.
;; Changed to "C-c h". Note: We must set "C-c h" globally, because we
;; cannot change `helm-command-prefix-key' once `helm-config' is loaded.
(global-set-key (kbd "C-c h") 'helm-command-prefix)
(global-unset-key (kbd "C-x c"))

;; (when (executable-find "curl")
;; (setq helm-google-suggest-use-curl-p t))

(setq helm-split-window-in-side-p           t ; open helm buffer inside current window, not occupy whole other window
      helm-move-to-line-cycle-in-source     t ; move to end or beginning of source when reaching top or bottom of source.
      helm-ff-search-library-in-sexp        t ; search for library in `require' and `declare-function' sexp.
      helm-scroll-amount                    8 ; scroll 8 lines other window using M-<next>/M-<prior>
      helm-ff-file-name-history-use-recentf t
      helm-echo-input-in-header-line t)

(setq helm-autoresize-max-height 0)
(setq helm-autoresize-min-height 20)
(helm-autoresize-mode 1)
(define-key helm-map (kbd "TAB") 'helm-execute-persistent-action) ; rebind tab to do persistent action
(define-key helm-map (kbd "C-i") 'helm-execute-persistent-action) ; make TAB works in terminal
(define-key helm-map (kbd "C-z")  'helm-select-action) ; list actions using C-z
(global-set-key (kbd "M-x") 'helm-M-x) 
(setq helm-M-x-fuzzy-match t) ;; optional fuzzy matching for helm-M-x
(global-set-key (kbd "M-y") 'helm-show-kill-ring)
(global-set-key (kbd "C-x b") 'helm-mini)
(setq helm-buffers-fuzzy-matching t
      helm-recentf-fuzzy-match    t)
(global-set-key (kbd "C-x C-f") 'helm-find-files)
(setq helm-semantic-fuzzy-match t
      helm-imenu-fuzzy-match    t) 
(setq helm-locate-fuzzy-match t)
(global-set-key (kbd "C-c h o") 'helm-occur)
(setq helm-apropos-fuzzy-match t)
(global-set-key (kbd "C-h SPC") 'helm-all-mark-rings)


;; With this, see data frame variables in Helm instead
;; of using company tooltips
(autoload 'helm-company "helm-company")
(eval-after-load 'company
  '(progn
     (define-key company-mode-map (kbd "C-:") 'helm-company)
     (define-key company-active-map (kbd "C-:") 'helm-company)))


;; Swiper: advanced way to search 
(require 'swiper)
(global-unset-key (kbd "C-s"))
(global-set-key (kbd "C-s") 'swiper)
(helm-mode 1)

;; ========== Projectile ===========
;; This library provides easy project management and navigation

(projectile-mode +1)
(define-key projectile-mode-map (kbd "s-p") 'projectile-command-map)
(define-key projectile-mode-map (kbd "C-c p") 'projectile-command-map)

;; helm-projectile
(require 'helm-projectile)
(setq projectile-completion-system 'helm)
(helm-projectile-on)

;; ;; ========== Docker ===========
(require 'dockerfile-mode)

;; ;; ========== Markdown ===========
(require 'markdown-mode)

;; ;; ========== Python ====================
(use-package conda
  :ensure t
  :init
  (setq conda-anaconda-home (expand-file-name "/home/razielar/bin/miniconda3"))
  :config
  ;; If you want interactive shell support, include:
  (conda-env-initialize-interactive-shells)
  ;; If you want eshell support, include:
  (conda-env-initialize-eshell)
  ;; If you want auto-activation, include:
  (conda-env-autoactivate-mode t)
  ;; Activate the project/virtual env you want to use.
  ;; Via M-x conda-env-activate RET analyticd-pysystemtrade
  ;; or
  ;; (conda-env-activate "analyticd-pysystemtrade")
  )

(elpy-enable)
;; ;; (defun py34c ()
;; ;;   (interactive)
;; ;;   (pyvenv-activate "~/.conda/envs/py34c/")
;; ;;   )

;; ;; (add-hook 'python-mode-hook 'anaconda-mode)
;; ;; (add-hook 'python-mode-hook 'anaconda-eldoc-mode)

(setq python-shell-interpreter "jupyter"
      python-shell-interpreter-args "console --simple-prompt"
      python-shell-prompt-detect-failure-warning nil)
(add-to-list 'python-shell-completion-native-disabled-interpreters
             "jupyter")

;; enable autopep8 formatting on save
(require 'py-autopep8)
(add-hook 'elpy-mode-hook 'py-autopep8-enable-on-save)

;; Redefine Elpy's default bindings for movement and evaluation
(define-key elpy-mode-map (kbd "<M-down>") nil)
(define-key elpy-mode-map (kbd "<M-up>") nil) 
(define-key elpy-mode-map (kbd "<M-right>") nil)
(define-key elpy-mode-map (kbd "<M-left>") nil)
(define-key elpy-mode-map (kbd "C-c s") 'elpy-nav-move-line-or-region-down)
(define-key elpy-mode-map (kbd "C-c w") 'elpy-nav-move-line-or-region-up) 
(define-key elpy-mode-map (kbd "C-c d") 'elpy-nav-indent-shift-right)
(define-key elpy-mode-map (kbd "C-c a") 'elpy-nav-indent-shift-left)
(define-key elpy-mode-map (kbd "<C-up>") nil)
(define-key elpy-mode-map (kbd "<C-down>") nil)





