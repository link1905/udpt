import { useEffect, useState } from "react";
import { requestGetAllAccounts } from "../../../services/account/get-all-accounts";
import { AccountFields } from "../../../services/account/account.client";
import { Model } from "../../../services/client";
import { Table, Button, Modal, Text } from "@mantine/core";
import { format } from "date-fns";
import { requestDeleteAccount } from "../../../services/account/delete-account";
import { Pagination } from "@mantine/core";
import { IconTrash } from "@tabler/icons-react";
import { Alert } from "@mantine/core";
import { IconAlertCircle } from "@tabler/icons-react";
const ManageAccounts = () => {
  const [accounts, setAccounts] = useState<Model<AccountFields>[]>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [selectedAccount, setSelectedAccount] =
    useState<Model<AccountFields> | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const pageSize = 4;
  const handleUsernameClick = (account: Model<AccountFields>) => {
    setSelectedAccount(account);
    setIsModalOpen(true);
  };
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState<boolean>(false);
  const [accountToDelete, setAccountToDelete] =
    useState<Model<AccountFields> | null>(null);
  const handleOpenDeleteModal = (account: Model<AccountFields>) => {
    setAccountToDelete(account);
    setIsDeleteModalOpen(true);
  };
  const [showAlert, setShowAlert] = useState(false);

  const handleCloseDeleteModal = () => {
    setIsDeleteModalOpen(false);
    setAccountToDelete(null);
  };

  useEffect(() => {
    requestGetAllAccounts()
      .then((accountsResponse) => {
        setAccounts(accountsResponse);
      })
      .catch((error) => {
        console.error("Error fetching accounts:", error);
      });
  }, []);

  const handleDeleteAccount = (pk: number) => {
    const accountToDelete = accounts.find((account) => account.pk === pk);

    if (accountToDelete?.fields.is_staff) {
      setShowAlert(true);
  
      
      setTimeout(() => {
        setShowAlert(false);
      }, 2000);
  
      return;
    }
    requestDeleteAccount(pk)
      .then(() => {
        const updatedAccounts = accounts.filter((account) => account.pk !== pk);
        setAccounts(updatedAccounts);
      })
      .catch((error) => {
        console.error("Error deleting account:", error);
      });
  };

  const columns = [
    {
      name: "username",
      title: "Username",
      render: (rowData: Model<AccountFields>) => (
        <a
          href="#"
          className="text-blue-500"
          onClick={() => handleUsernameClick(rowData)}
        >
          {rowData.fields.username}
        </a>
      ),
    },
    { name: "email", title: "Email" },
    {
      name: "date_joined",
      title: "Date joined",
      render: (rowData: Model<AccountFields>) =>
        format(new Date(rowData.fields.date_joined), "MMMM dd, yyyy"),
    },

    {
      title: "Delete",
      render: (rowData: Model<AccountFields>) => (
        <Button
          size="sm"
          variant="outline"
          color="red"
          onClick={() => handleOpenDeleteModal(rowData)}
        >
          <IconTrash /> Delete
        </Button>
      ),
    },
  ];

  const totalAccounts = accounts.length;
  const totalPages = Math.ceil(totalAccounts / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const visibleAccounts = accounts.slice(startIndex, startIndex + pageSize);

  return (
    <>
      {showAlert && (
        <Alert
          className="w-[30%] m-auto"
          icon={<IconAlertCircle size="1rem" />}
          title="KHÔNG ĐƯỢC XÓA"
          color="red"
          radius="lg"
          withCloseButton
          variant="filled"
        >
          Bạn không có quyền xóa tài khoản ADMIN
        </Alert>
      )}

      {selectedAccount && (
        <Modal
          opened={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          title="Account Details"
        >
          <div>
            <Text>
              <b>Username</b>: {selectedAccount.fields.username}
            </Text>
            <Text>
              <b>Email</b>: {selectedAccount.fields.email}
            </Text>
            <Text>
              <b>First Name</b>: {selectedAccount.fields.first_name}
            </Text>
            <Text>
              <b>Last Name</b>: {selectedAccount.fields.last_name}
            </Text>
            <Text>
              <b>Date Joined: </b>
              {format(
                new Date(selectedAccount.fields.date_joined),
                "MMMM dd, yyyy"
              )}
            </Text>

            <Button
              className="mt-3 bg-blue-500 text-white border-blue-500"
              onClick={() => setIsModalOpen(false)}
            >
              Close
            </Button>
          </div>
        </Modal>
      )}
      {accountToDelete && (
        <Modal
          opened={isDeleteModalOpen}
          onClose={handleCloseDeleteModal}
          title="Confirm Delete"
          size="sm"
          overlayOpacity={0.6}
        >
          <Text size="lg" className="mb-4">
            Are you sure you want to delete this account?
          </Text>
          <div className="flex justify-center space-x-3">
            <Button
              size="sm"
              variant="outline"
              color="red"
              onClick={() => {
                handleDeleteAccount(accountToDelete.pk);
                handleCloseDeleteModal();
              }}
            >
              Delete
            </Button>
            <Button
              size="sm"
              onClick={handleCloseDeleteModal}
              className="bg-blue-500 text-white border-blue-500"
            >
              Cancel
            </Button>
          </div>
        </Modal>
      )}

      <Table
        striped
        highlightOnHover
        withBorder
        withColumnBorders
        horizontalSpacing="xl"
        verticalSpacing="lg"
      >
        <thead>
          <tr>
            {columns.map((column) => (
              <th
                key={column.name}
                style={{
                  textAlign: "center",
                  color: "black",
                  fontWeight: "bold",
                }}
              >
                {column.title || column.name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {visibleAccounts.map((account) => (
            <tr key={account.pk}>
              {columns.map((column) => (
                <td key={column.name} className="px-4 py-2 text-center">
                  {column.render
                    ? column.render(account)
                    : account.fields[column.name]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </Table>

      <Pagination
        className="justify-center mt-[40px]"
        total={totalPages}
        value={currentPage}
        onChange={setCurrentPage}
      />
    </>
  );
};

export default ManageAccounts;
