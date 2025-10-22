// Simple helper to combine class names conditionally
export function cn(...classes: any[]) {
    return classes.filter(Boolean).join(" ");
  }