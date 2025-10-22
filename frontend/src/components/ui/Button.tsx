import React from "react";
import { cn } from "../../lib/utils";

export const Button = ({ children, className, ...props }: any) => (
  <button
    {...props}
    className={cn(
      "rounded-lg px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 transition text-sm font-medium",
      className
    )}
  >
    {children}
  </button>
);