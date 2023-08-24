import { Menu, Button } from "@mantine/core";
import {  useNavigate } from "react-router-dom";

const Dropdown = ({ isStaff }) => {
  const navigate = useNavigate();
  const handleManageThreads = () => {
    navigate("/admin/manage-threads");
  };
  const handleManageCategories = () => {
    navigate("/admin/manage-categories");
  };
  const handleManageTags = () => {
    navigate("/admin/manage-tags");
  };
  const handleManageAccounts = () => {
    navigate("/admin/manage-accounts");
  };
  return (
    <Menu shadow="md" width={200}>
      <Menu.Target>
        <Button className="bg-blue-500 text-white border-blue-500 ml-[20px]">Management</Button>
      </Menu.Target>

      {isStaff && ( 
        <Menu.Dropdown>
          <Menu.Label>Admin Menu</Menu.Label>
          <Menu.Item onClick={handleManageThreads}>Manage Threads</Menu.Item>
          <Menu.Item onClick={handleManageCategories}>Manage Categories</Menu.Item>
          <Menu.Item onClick={handleManageTags}>Manage tags</Menu.Item>
          <Menu.Item onClick={handleManageAccounts}>Manage accounts</Menu.Item>
        </Menu.Dropdown>
      )}
    </Menu>
  );
};

export default Dropdown;
