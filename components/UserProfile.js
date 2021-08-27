import React from "react";

export default function UserProfile({ user }) {
  return <pre>{JSON.stringify(user, null, 2)}</pre>;
}
