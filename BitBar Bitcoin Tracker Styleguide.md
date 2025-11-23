# **Bitcoin Tracker UI Style Guide**

Platform Target: Python Desktop App (macOS Style)  
Design Source: React Prototype v2.2

## **1\. Color Palette**

### **Brand Colors**

* **Bitcoin Orange:** \#F7931A (Logo background)  
* **Active Blue:** \#3B82F6 (Selected currency, accents)  
* **Trend Green:** \#22C55E (Positive change)  
* **Trend Red:** \#EF4444 (Negative change)

### **Theme Modes**

#### **Light Mode (Default)**

* **Surface Background:** \#FFFFFF (90% Opacity)  
* **Primary Text:** \#1E293B (Slate 800\)  
* **Secondary Text:** \#64748B (Slate 500 \- used for labels)  
* **Borders/Dividers:** \#E2E8F0 (Slate 200\)  
* **Hover State:** rgba(0, 0, 0, 0.05)

#### **Dark Mode**

* **Surface Background:** \#0F172A (Slate 900 \- 90% Opacity)  
* **Primary Text:** \#FFFFFF  
* **Secondary Text:** \#94A3B8 (Slate 400\)  
* **Borders/Dividers:** \#334155 (Slate 700\)  
* **Hover State:** rgba(255, 255, 255, 0.1)

#### **Menu Bar Specifics**

* **Bar Background:** \#1E1E1E (80% Opacity)  
* **Bar Text:** \#FFFFFF  
* **Icon Color:** \#EAB308 (Yellow 500\)

## **2\. Typography**

**Font Family:** System Sans-Serif (San Francisco on macOS, Segoe UI on Windows)

| Element | Size (px) | Weight | Tracking/Style | Color Context |
| :---- | :---- | :---- | :---- | :---- |
| **Menu Bar Price** | 13px | Medium (500) | Normal | White |
| **Main Price (Header)** | 24px | Bold (700) | Tight (-0.025em) | Primary |
| **Section Headers** | 10px | Bold (700) | Wide (Uppercase) | Secondary (50% Opacity) |
| **Stats Value** | 14px | Semibold (600) | Tabular Nums | Primary |
| **Currency Button** | 12px | Medium (500) | Normal | Mixed |
| **Footer Text** | 9px | Regular (400) | Normal | Secondary |

## **3\. Layout & Dimensions**

### **Main Window (Dropdown)**

* **Width:** 320px  
* **Corner Radius:** 12px (matches rounded-xl)  
* **Shadow:** Soft spread shadow (CSS box-shadow: 0 25px 50px \-12px rgba(0, 0, 0, 0.25))

### **Spacing System (4px Base)**

* **Padding (Container):** 16px (Header) / 12px (Content) / 8px (Menu Items)  
* **Gaps:** 8px (Grid gaps), 4px (Icon spacing)

### **Borders**

* **Width:** 1px  
* **Color:** See Theme Modes above.  
* **Triangle Pointer:** \~12px size, positioned top-right.

## **4\. Components**

### **A. Header Section**

* **Layout:** Flex row (Logo \+ Text Group) \+ Action Buttons (Right aligned).  
* **Logo:** 32x32px Circle, Center aligned text.  
* **Trend Pill:** Displayed next to or below price depending on width constraints.

### **B. Stats Grid**

* **Structure:** 2x2 Grid.  
* **Separators:** 1px borders between cells (effectively a crosshair grid).  
* **Alignment:** Center text, center content.

### **C. Currency Selector**

* **Structure:** 3 Columns.  
* **Button Height:** \~28px.  
* **State Styles:**  
  * *Active:* Background \#3B82F6, Text White, Border \#2563EB.  
  * *Inactive:* Transparent border, Background opacity 5%.

### **D. Menu List Items**

* **Height:** \~36px.  
* **Corner Radius:** 8px.  
* **Layout:** Icon (Left) \+ Label (Left) \+ Value/Toggle (Right).  
* **Interaction:** Background color change on hover (see Color Palette).

## **5\. Icons (Lucide Style)**

* **Stroke Width:** 2px  
* **Size:**  
  * Standard Icon: 14px  
  * Action Button Icon: 16px  
* **Required Icons:**  
  * RefreshCw (Refresh)  
  * Moon / Sun (Theme Toggle)  
  * ExternalLink (Website)  
  * Info (About)  
  * TrendingUp / TrendingDown (Price indicators)