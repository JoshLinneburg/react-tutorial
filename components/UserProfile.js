import React from "react";

export default function UserProfile({ user }) {
  return JSON.stringify(user, null, 2);
}
