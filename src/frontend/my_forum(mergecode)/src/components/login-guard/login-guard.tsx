import { PropsWithChildren } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  authRequestQueryKey,
  requestAuthRefresh,
} from "../../services/account/auth-refresh.ts";
import { LoadingOverlay } from "@mantine/core";
import { Navigate } from "react-router-dom";
export function LoginGuard({ children }: PropsWithChildren<{}>) {
  const { error, isLoading } = useQuery(
    authRequestQueryKey,
    requestAuthRefresh,
    {
      retry: 0,
    },
  );
  if (isLoading) {
    return <LoadingOverlay visible />;
  }
  if (error) {
    return <Navigate to="/signin" />;
  }
  
  return <>{children}</>;
}
