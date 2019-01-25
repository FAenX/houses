import  React, { Component } from  'react';

import  ManagersService  from  './ManagersService';

const  managersService  =  new  ManagersService();

class  ManagersList  extends  Component {

    constructor(props) {
        super(props);
        this.state  = {
            managers: [],
            nextPageURL:  ''
        };
        this.nextPage  =  this.nextPage.bind(this);
        this.handleDelete  =  this.handleDelete.bind(this);
    }
	componentDidMount() {
	    var  self  =  this;
	    managersService.getManagers().then(function (result) {
		console.log(result);
		self.setState({ managers:  result.data, nextPageURL:  result.nextlink})
	    });
	}
	handleDelete(e,pk){
	    var  self  =  this;
	    managersService.deleteCustomer({pk :  pk}).then(()=>{
		var  newArr  =  self.state.Managers.filter(function(obj) {
		    return  obj.pk  !==  pk;
		});

		self.setState({Managers:  newArr})
	    });
	}

	nextPage(){
		var  self  =  this;
		console.log(this.state.nextPageURL);
		managersService.getManagersByURL(this.state.nextPageURL).then((result) => {
		    self.setState({ Managers:  result.data, nextPageURL:  result.nextlink})
		});
	}
	render() {

		return (
		    <div  className="Managers--list">
		        <table  className="table">
		        <thead  key="thead">
		        <tr>
		            <th>#</th>
		            <th>First Name</th>
		            <th>Last Name</th>
		            <th>Phone</th>
		            <th>Email</th>
		            <th>Address</th>
		            <th>Description</th>
		            <th>Actions</th>
		        </tr>
		        </thead>
		        <tbody>
		        {this.state.managers.map( c  =>
		            <tr  key={c.pk}>
		            <td>{c.pk}  </td>
		            <td>{c.first_name}</td>
		            <td>{c.last_name}</td>
		            <td>{c.phone}</td>
		            <td>{c.email}</td>
		            <td>{c.address}</td>
		            <td>{c.description}</td>
		            <td>
		            <button  onClick={(e)=>  this.handleDelete(e,c.pk) }> Delete</button>
		            <a  href={"/manager/" + c.pk}> Update</a>
		            </td>
		        </tr>)}
		        </tbody>
		        </table>
		        <button  className="btn btn-primary"  onClick=  {  this.nextPage  }>Next</button>
		    </div>
		    );
	  } 
}
export  default  ManagersList;
