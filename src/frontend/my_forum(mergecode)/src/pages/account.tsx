import {
  Grid,
  Group,
  Stack,
  TextInput,
  Button,
  Box,
  LoadingOverlay,
  Avatar,
  PasswordInput,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  authRequestQueryKey,
  requestAuthRefresh,
} from "../services/account/auth-refresh.ts";
import { useState, useEffect } from "react";
import { requestUpdateAccount } from "../services/account/update-account.ts";
import { useRef } from "react";
import { requestChangePassword } from "../services/account/change-password.ts";
import CustomAlert from "../components/custom_alert/CustomAlert.tsx";
export interface AccountFormData {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  oldPassword: string;
  newPassword: string;
  confirmNewPassword: string;
}

export function AccountPage() {
  const [showAlertSuccess, setShowAlertSuccess] = useState<boolean>(false);
  const [updateSuccess, setUpdateSuccess] = useState<{
    first_name: boolean;
    last_name: boolean;
    email: boolean;
    newPassword: boolean;
  }>({
    first_name: false,
    last_name: false,
    email: false,
    newPassword: false,
  });
  const [updateError, setUpdateError] = useState<{
    email: boolean;
    oldPassword: boolean;
    newPassword: boolean;
  }>({
    email: false,
    oldPassword: false,
    newPassword: false,
  });
  const inputRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();
  const { mutate, isLoading: isUpdating } = useMutation(requestUpdateAccount, {
    async onSuccess() {
      await queryClient.invalidateQueries(authRequestQueryKey);
    },
  });
  const { data, isLoading } = useQuery(
    authRequestQueryKey,
    requestAuthRefresh,
    {
      retry: 0,
    },
  );
  const form = useForm<AccountFormData>({
    initialValues: {
      username: data?.fields?.username ?? "",
      email: data?.fields?.email ?? "",
      first_name: data?.fields?.first_name ?? "",
      last_name: data?.fields?.last_name ?? "",
      oldPassword: "",
      newPassword: "",
      confirmNewPassword: "",
    },
    validate: {
      username: (value) => !value,
      email: (value) => !value,
      first_name: (value) => !value,
      last_name: (value) => !value,
    },
  });

  async function handleSubmit(values: AccountFormData) {
    if (values.newPassword !== values.confirmNewPassword) {
      return;
    }

    await mutate({
      id: data?.pk ?? 0,
      ...values,
    });

    requestChangePassword({
      oldPassword: values.oldPassword,
      newPassword: values.newPassword,
      confirmNewPassword: values.confirmNewPassword,
    });

    if (values.first_name !== data?.fields?.first_name) {
      setUpdateSuccess((prev) => ({ ...prev, first_name: true }));
    }
    if (values.last_name !== data?.fields?.last_name) {
      setUpdateSuccess((prev) => ({ ...prev, last_name: true }));
    }
    if (values.email !== data?.fields?.email) {
      setUpdateSuccess((prev) => ({ ...prev, email: true }));
    }
    if (values.newPassword !== "") {
      setUpdateSuccess((prev) => ({ ...prev, newPassword: true }));
    }

    setShowAlertSuccess(true);
    setTimeout(() => {
      setShowAlertSuccess(false);
    }, 3000);
  }

  return (
    <Box>
      <LoadingOverlay visible={isLoading} />
      <Grid>
        <Grid.Col span={3} sx={{ textAlign: "center" }}>
          <Group position="center">
            <input
              type="file"
              accept="image/png, image/gif, image/jpeg"
              ref={inputRef}
              style={{ display: "none" }}
              onChange={(e) => {
                mutate({
                  id: data?.pk ?? 0,
                  username: data?.fields?.username ?? "",
                  avatar: e.target?.files?.[0],
                });
              }}
            />
            <Avatar
              src={`${import.meta.env.VITE_API_URL}account/media/${data?.fields
                ?.avatar}`}
              sx={{ width: 200, height: 200 }}
              onClick={() => inputRef.current?.click()}
            />
          </Group>
        </Grid.Col>
        <Grid.Col span={9}>
          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack>
              <TextInput
                placeholder="Username"
                label="Username"
                disabled
                {...form.getInputProps("username")}
              />
              <Group grow>
                <TextInput
                  placeholder="First name"
                  label="First name"
                  withAsterisk
                  {...form.getInputProps("first_name")}
                />
                <TextInput
                  placeholder="Last name"
                  label="Last name"
                  withAsterisk
                  {...form.getInputProps("last_name")}
                />
              </Group>
              <TextInput
                placeholder="Email"
                label="Email"
                withAsterisk
                {...form.getInputProps("email")}
              />
              <TextInput
                type="password"
                placeholder="Old Password"
                label="Old Password"
                withAsterisk
                {...form.getInputProps("oldPassword")}
              />
              <PasswordInput
                placeholder="New Password"
                label="New Password"
                withAsterisk
                {...form.getInputProps("newPassword")}
              />
              <PasswordInput
                placeholder="Confirm New Password"
                label="Confirm New Password"
                withAsterisk
                {...form.getInputProps("confirmNewPassword")}
              />
              {showAlertSuccess && (
                <div className="fixed top-12 right-0 p-4 z-[9999] ">
                  {updateSuccess.first_name && (
                    <CustomAlert
                      color="green"
                      title="Success"
                      message="Update first name successfully!"
                    />
                  )}

                  {updateSuccess.last_name && (
                    <CustomAlert
                      color="green"
                      title="Success"
                      message="Update last name successfully!"
                    />
                  )}
                  {updateSuccess.email && (
                    <CustomAlert
                      color="green"
                      title="Success"
                      message="Update email successfully!"
                    />
                  )}
                  {updateSuccess.newPassword && (
                    <CustomAlert
                      color="green"
                      title="Success"
                      message="Update password successfully!"
                    />
                  )}
                </div>
              )}
              <Group>
                <Button
                  className="bg-blue-500 text-white border-blue-500"
                  loading={isUpdating}
                  type="submit"
                >
                  Submit
                </Button>
              </Group>
            </Stack>
          </form>
        </Grid.Col>
      </Grid>
    </Box>
  );
}
